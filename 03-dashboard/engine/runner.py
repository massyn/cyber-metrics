"""Run a metric's queries against posture's parquet files with DuckDB."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

import duckdb
import jinja2
import pandas as pd

from engine.definitions import MetricDefinition

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = ("resource", "resource_type", "compliance", "detail")
TABLE_NAME = re.compile(r"^[a-z0-9_]+$")


class QueryError(RuntimeError):
    """A metric query could not be run, or returned the wrong shape."""


@dataclass
class MetricRun:
    definition: MetricDefinition
    detail: pd.DataFrame
    errors: list[str] = field(default_factory=list)


def resolve_source(data_path: Path, table: str) -> Path | None:
    """Find a table's parquet file: <table>.parquet, else the latest <table>/<YYYY.MM.DD>.parquet (--history)."""
    flat = data_path / f"{table}.parquet"
    if flat.is_file():
        return flat
    history = sorted((data_path / table).glob("*.parquet"))
    return history[-1] if history else None


def run_query(query: str, data_path: Path) -> pd.DataFrame:
    """Render a metric query's {{ ref('table') }} calls to DuckDB views over the parquet files, and run it."""
    missing: list[str] = []
    with duckdb.connect() as con:

        def ref(table: str) -> str:
            if not TABLE_NAME.match(table):
                raise QueryError(f"Invalid table name {table!r}")
            path = resolve_source(data_path, table)
            if path is None:
                missing.append(table)
            else:
                con.read_parquet(str(path)).create_view(table)
            return table

        try:
            sql = (
                jinja2.Environment(undefined=jinja2.StrictUndefined)
                .from_string(query)
                .render(ref=ref)
            )
        except jinja2.TemplateError as exc:
            raise QueryError(f"Template error: {exc}") from exc
        if missing:
            raise QueryError(
                f"Source table not found: {', '.join(sorted(set(missing)))}"
            )

        try:
            df = con.sql(sql).df()
        except duckdb.Error as exc:
            raise QueryError(str(exc)) from exc

    absent = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if absent:
        raise QueryError(
            f"Query did not return required column(s): {', '.join(absent)}"
        )
    return df


def run_metric(definition: MetricDefinition, data_path: Path) -> MetricRun:
    """Run every query of a metric and combine the results. A failing query is recorded and skipped."""
    frames, errors = [], []
    if definition.enabled:
        for number, query in enumerate(definition.queries, start=1):
            try:
                frames.append(run_query(query, data_path))
            except QueryError as exc:
                logger.warning(
                    "Metric %s query %d skipped: %s", definition.metric_id, number, exc
                )
                errors.append(f"Query {number}: {exc}")

    columns = list(REQUIRED_COLUMNS)
    detail = (
        pd.concat(frames, ignore_index=True)
        if frames
        else pd.DataFrame(columns=columns)
    )
    detail["compliance"] = pd.to_numeric(detail["compliance"], errors="coerce").astype(
        float
    )
    invalid = int(detail["compliance"].isna().sum())
    if invalid:
        errors.append(
            f"{invalid} row(s) had a non-numeric compliance value and were dropped"
        )
        detail = detail.dropna(subset=["compliance"])
    for column in ("resource", "resource_type", "detail"):
        detail[column] = detail[column].astype("string").fillna("")

    return MetricRun(definition, detail[columns].reset_index(drop=True), errors)
