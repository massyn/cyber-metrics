from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from engine.definitions import DefinitionError, load_definitions, parse_definition
from engine.runner import (
    REQUIRED_COLUMNS,
    QueryError,
    resolve_source,
    run_metric,
    run_query,
)

BASE = {
    "metric_id": "x",
    "title": "X",
    "category": "Data Protection",
    "type": "control",
    "description": "d",
    "how": "h",
    "weight": 1,
    "indicator": False,
}


def test_slo_list_is_minimum_then_target() -> None:
    definition = parse_definition({**BASE, "slo": [0.8, 0.95]}, "metric_x.yml")
    assert (definition.slo_min, definition.slo) == (0.8, 0.95)


def test_single_slo_is_used_for_both() -> None:
    definition = parse_definition({**BASE, "slo": 0.9}, "metric_x.yml")
    assert (definition.slo_min, definition.slo) == (0.9, 0.9)


def test_query_as_single_string_is_rejected() -> None:
    with pytest.raises(DefinitionError, match="list"):
        parse_definition({**BASE, "query": "SELECT 1"}, "metric_x.yml")


def test_missing_field_is_rejected() -> None:
    raw = {key: value for key, value in BASE.items() if key != "category"}
    with pytest.raises(DefinitionError, match="category"):
        parse_definition(raw, "metric_x.yml")


def test_how_is_optional() -> None:
    raw = {key: value for key, value in BASE.items() if key != "how"}
    assert parse_definition(raw, "metric_x.yml").how == ""


def test_load_definitions_skips_invalid_files(metrics_path: Path) -> None:
    (metrics_path / "metric_broken.yml").write_text(
        "metric_id: broken\n", encoding="utf-8"
    )
    ids = [d.metric_id for d in load_definitions(metrics_path)]
    assert ids == ["dp_encryption", "im_mfa", "ns_waf"]


def test_resolve_source_prefers_flat_file_then_latest_history(tmp_path: Path) -> None:
    frame = pd.DataFrame({"a": [1]})
    (tmp_path / "t").mkdir()
    frame.to_parquet(tmp_path / "t" / "2026.01.01.parquet")
    frame.to_parquet(tmp_path / "t" / "2026.02.01.parquet")
    assert resolve_source(tmp_path, "t") == tmp_path / "t" / "2026.02.01.parquet"

    frame.to_parquet(tmp_path / "t.parquet")
    assert resolve_source(tmp_path, "t") == tmp_path / "t.parquet"
    assert resolve_source(tmp_path, "missing") is None


def test_run_query_requires_the_standard_columns(data_path: Path) -> None:
    with pytest.raises(QueryError, match="resource_type, compliance, detail"):
        run_query("SELECT hostname AS resource FROM {{ ref('acme_hosts') }}", data_path)


def test_run_query_reports_missing_table(data_path: Path) -> None:
    with pytest.raises(QueryError, match="acme_nope"):
        run_query("SELECT * FROM {{ ref('acme_nope') }}", data_path)


def test_run_query_rejects_unsafe_table_names(data_path: Path) -> None:
    with pytest.raises(QueryError, match="Invalid table name"):
        run_query("SELECT * FROM {{ ref('x; DROP') }}", data_path)


def test_run_query_reports_sql_errors(data_path: Path) -> None:
    with pytest.raises(QueryError):
        run_query("SELECT nonsense FROM {{ ref('acme_hosts') }}", data_path)


def test_run_metric_keeps_good_queries_and_records_failures(
    metrics_path: Path, data_path: Path
) -> None:
    definition = next(
        d for d in load_definitions(metrics_path) if d.metric_id == "im_mfa"
    )
    run = run_metric(definition, data_path)
    assert run.detail["resource"].tolist() == ["alice", "bob"]
    assert run.detail["compliance"].tolist() == [1.0, 0.0]
    assert (
        len(run.errors) == 1
        and "Query 2" in run.errors[0]
        and "acme_missing" in run.errors[0]
    )


def test_run_metric_keeps_only_the_standard_columns(
    metrics_path: Path, data_path: Path
) -> None:
    definition = next(
        d for d in load_definitions(metrics_path) if d.metric_id == "dp_encryption"
    )
    run = run_metric(definition, data_path)
    assert run.detail.columns.tolist() == list(REQUIRED_COLUMNS)


def test_disabled_metric_runs_nothing(data_path: Path) -> None:
    raw = {
        **BASE,
        "enabled": False,
        "query": ["SELECT * FROM {{ ref('acme_missing') }}"],
    }
    run = run_metric(parse_definition(raw, "metric_x.yml"), data_path)
    assert run.detail.empty and run.errors == []
