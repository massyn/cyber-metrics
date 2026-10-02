from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import pytest

from engine.definitions import parse_definition
from scoring.detail import DetailFilters, build_detail
from scoring.scorecard import (
    ALL,
    BAD,
    GOOD,
    NO_DATA,
    WARNING,
    ScorecardFilters,
    build_page,
    build_summary,
    score,
    score_metric,
)
from scoring.store import MetricStore

DEFINITION = parse_definition(
    {
        "metric_id": "x",
        "title": "X",
        "category": "c",
        "type": "control",
        "description": "d",
        "how": "h",
        "weight": 1,
        "indicator": False,
        "slo": [0.5, 0.9],
    },
    "metric_x.yml",
)


@pytest.mark.parametrize(
    ("compliance", "status"),
    [
        ([1, 1, 1, 1, 1, 1, 1, 1, 1, 0], GOOD),
        ([1, 1, 1, 0], WARNING),
        ([1, 0, 0, 0], BAD),
        ([], NO_DATA),
    ],
)
def test_score_status_follows_slo(compliance: list[int], status: str) -> None:
    result = score(DEFINITION, pd.DataFrame({"compliance": compliance}, dtype=float))
    assert result.status == status
    assert result.total == len(compliance)


@pytest.fixture
def runs(metrics_path: Path, data_path: Path) -> list:
    return MetricStore(metrics_path, data_path).runs()


def scores(runs: list, filters: ScorecardFilters) -> dict[str, tuple]:
    return {
        r.definition.metric_id: (
            score_metric(r, filters).score.status,
            score_metric(r, filters).visible,
        )
        for r in runs
    }


def test_metrics_without_data_are_hidden_unless_asked_for(runs: list) -> None:
    assert scores(runs, ScorecardFilters()) == {
        "dp_encryption": (WARNING, True),
        "im_mfa": (BAD, True),
        "ns_waf": (NO_DATA, False),
    }
    assert scores(runs, ScorecardFilters(status=NO_DATA))["ns_waf"] == (NO_DATA, True)
    assert scores(runs, ScorecardFilters(status=NO_DATA))["im_mfa"] == (BAD, False)
    assert all(
        visible for _, visible in scores(runs, ScorecardFilters(status=ALL)).values()
    )


def test_score_note_explains_missing_data(runs: list) -> None:
    notes = {
        r.definition.metric_id: score_metric(r, ScorecardFilters()).note for r in runs
    }
    assert notes == {
        "dp_encryption": "",
        "im_mfa": "1 query error(s)",
        "ns_waf": "No query defined",
    }


def test_summary_counts_ignore_the_status_filter(runs: list) -> None:
    summary = build_summary(runs, ScorecardFilters(status=BAD))
    assert summary.status_counts == {GOOD: 0, WARNING: 1, BAD: 1, NO_DATA: 1}
    assert [c.category for c in summary.categories] == ["Identity Management"]


def test_summary_overall_and_categories_are_weighted(runs: list) -> None:
    summary = build_summary(runs, ScorecardFilters())
    # dp_encryption 0.75 (weight 1), im_mfa 0.5 (weight 3)
    assert summary.overall == pytest.approx((0.75 * 1 + 0.5 * 3) / 4)
    categories = {
        c.category: (c.value, c.status, c.metrics) for c in summary.categories
    }
    assert categories == {
        "Data Protection": (0.75, WARNING, 1),
        "Identity Management": (0.5, BAD, 1),
    }


def test_page_filters_definitions(runs: list) -> None:
    definitions = [r.definition for r in runs]
    page = build_page(definitions, ScorecardFilters(search="MFA"))
    assert [d.metric_id for d in page.definitions] == ["im_mfa"]
    page = build_page(definitions, ScorecardFilters(category="Data Protection"))
    assert [d.metric_id for d in page.definitions] == ["dp_encryption"]
    assert page.categories == [
        "Data Protection",
        "Identity Management",
        "Network Security",
    ]


def test_detail_filters_sorts_and_pages(runs: list) -> None:
    run = next(r for r in runs if r.definition.metric_id == "dp_encryption")
    page = build_detail(
        run, DetailFilters(sort="resource", descending=True), page_size=3
    )
    assert [r["resource"] for r in page.records] == ["web-2", "web-1", "db-2"]
    assert (page.page, page.pages, page.matching_records) == (1, 2, 4)

    failing = build_detail(run, DetailFilters(compliance="fail"), page_size=3)
    assert [(r["resource"], r["outcome"]) for r in failing.records] == [
        ("db-1", "fail")
    ]
    assert failing.score.total == 4  # the score ignores the compliance filter

    searched = build_detail(run, DetailFilters(search="WEB-"), page_size=10)
    assert [r["resource"] for r in searched.records] == ["web-1", "web-2"]


def test_detail_page_number_is_clamped(runs: list) -> None:
    run = next(r for r in runs if r.definition.metric_id == "dp_encryption")
    assert build_detail(run, DetailFilters(page=99), page_size=3).page == 2


def test_detail_filters_ignore_unknown_values() -> None:
    filters = DetailFilters.from_args(
        {"sort": "drop table", "compliance": "maybe", "page": "-3"}
    )
    assert (filters.sort, filters.compliance, filters.page) == ("compliance", "", 1)


def test_store_reruns_when_source_data_changes(
    metrics_path: Path, data_path: Path
) -> None:
    store = MetricStore(metrics_path, data_path)
    assert len(store.run("im_mfa").detail) == 2

    users = data_path / "acme_users.parquet"
    pd.DataFrame(
        {"login": ["alice", "bob", "carol"], "mfa": [True, False, True]}
    ).to_parquet(users)
    stat = users.stat()
    os.utime(users, ns=(stat.st_atime_ns, stat.st_mtime_ns + 1_000_000_000))
    assert len(store.run("im_mfa").detail) == 3


def test_store_runs_each_metric_once(
    metrics_path: Path, data_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import scoring.store

    calls: list[str] = []
    real_run_metric = scoring.store.run_metric

    def counting_run_metric(definition, path):
        calls.append(definition.metric_id)
        return real_run_metric(definition, path)

    monkeypatch.setattr(scoring.store, "run_metric", counting_run_metric)
    store = MetricStore(metrics_path, data_path)
    assert store.cached_runs() == []
    store.run("im_mfa")
    store.run("im_mfa")
    assert calls == ["im_mfa"]
    assert [r.definition.metric_id for r in store.cached_runs()] == ["im_mfa"]
    assert store.run("nope") is None
