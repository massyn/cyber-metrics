"""Score each metric against its SLO, and summarise the scorecard by status and category."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass

import pandas as pd

from engine.definitions import MetricDefinition
from engine.runner import MetricRun

GOOD, WARNING, BAD, NO_DATA = "good", "warning", "bad", "no_data"
STATUSES = (GOOD, WARNING, BAD, NO_DATA)
ALL = "all"  # status filter value that shows every metric, including those without data


@dataclass(frozen=True)
class Score:
    total: int
    passed: float
    value: float | None
    status: str


def rate(value: float | None, slo_min: float | None, slo: float | None) -> str:
    """Good at or above the SLO target, warning at or above the SLO minimum, else bad."""
    if value is None:
        return NO_DATA
    if slo is None or value >= slo:
        return GOOD
    if slo_min is None or value >= slo_min:
        return WARNING
    return BAD


def score(definition: MetricDefinition, detail: pd.DataFrame) -> Score:
    """passed / total, rated against the metric's SLO."""
    total = len(detail)
    if total == 0:
        return Score(0, 0.0, None, NO_DATA)
    passed = float(detail["compliance"].sum())
    value = passed / total
    return Score(total, passed, value, rate(value, definition.slo_min, definition.slo))


@dataclass(frozen=True)
class ScorecardFilters:
    category: str = ""
    type: str = ""
    status: str = ""  # "" shows every metric with data, ALL shows every metric
    search: str = ""

    @classmethod
    def from_args(cls, args: Mapping[str, str]) -> ScorecardFilters:
        status = args.get("status", "")
        return cls(
            category=args.get("category", ""),
            type=args.get("type", ""),
            status=status if status in (*STATUSES, ALL) else "",
            search=args.get("search", "").strip(),
        )

    def as_args(self, **overrides: str) -> dict[str, str]:
        """The active filters as URL arguments, with any overrides (e.g. a different status)."""
        args = {
            "category": self.category,
            "type": self.type,
            "status": self.status,
            "search": self.search,
            **overrides,
        }
        return {key: value for key, value in args.items() if value}

    def matches(self, definition: MetricDefinition) -> bool:
        """Every filter except status, which needs the metric's score."""
        if self.category and definition.category != self.category:
            return False
        if self.type and definition.type != self.type:
            return False
        needle = self.search.lower()
        return (
            not needle
            or needle in definition.title.lower()
            or needle in definition.metric_id.lower()
        )

    def matches_status(self, metric_score: Score) -> bool:
        if self.status == ALL:
            return True
        if self.status:
            return metric_score.status == self.status
        return metric_score.status != NO_DATA


@dataclass(frozen=True)
class ScorecardPage:
    """What the scorecard needs before any metric has run."""

    definitions: list[MetricDefinition]
    categories: list[str]
    types: list[str]


def build_page(
    definitions: list[MetricDefinition], filters: ScorecardFilters
) -> ScorecardPage:
    return ScorecardPage(
        definitions=sorted(
            (d for d in definitions if filters.matches(d)),
            key=lambda d: (d.category, d.title),
        ),
        categories=sorted({d.category for d in definitions}),
        types=sorted({d.type for d in definitions}),
    )


@dataclass(frozen=True)
class MetricScore:
    definition: MetricDefinition
    score: Score
    errors: list[str]
    note: str
    visible: bool  # whether it passes the status filter


def score_metric(run: MetricRun, filters: ScorecardFilters) -> MetricScore:
    definition = run.definition
    metric_score = score(definition, run.detail)
    if not definition.enabled:
        note = "Disabled"
    elif not definition.queries:
        note = "No query defined"
    elif run.errors:
        note = f"{len(run.errors)} query error(s)"
    elif metric_score.total == 0:
        note = "No matching resources"
    else:
        note = ""
    return MetricScore(
        definition,
        metric_score,
        run.errors,
        note,
        filters.matches_status(metric_score),
    )


@dataclass(frozen=True)
class CategoryScore:
    category: str
    value: float
    status: str
    metrics: int


@dataclass(frozen=True)
class Summary:
    overall: float | None
    status_counts: dict[str, int]
    categories: list[CategoryScore]


def weighted(scores: Iterable[MetricScore]) -> tuple[float, float, float, int] | None:
    """Weighted score, SLO minimum and SLO target of the metrics with data, excluding indicators."""
    counted = [
        s for s in scores if s.score.value is not None and not s.definition.indicator
    ]
    total_weight = sum(s.definition.weight for s in counted)
    if not total_weight:
        return None

    def average(values: list[float]) -> float:
        return (
            sum(v * s.definition.weight for v, s in zip(values, counted)) / total_weight
        )

    return (
        average([s.score.value for s in counted]),
        average([s.definition.slo_min or 0.0 for s in counted]),
        average([s.definition.slo or 0.0 for s in counted]),
        len(counted),
    )


def build_summary(runs: list[MetricRun], filters: ScorecardFilters) -> Summary:
    """Status counts across the metrics matching every filter but status; overall and category scores
    across the metrics shown."""
    scores = [
        score_metric(run, filters) for run in runs if filters.matches(run.definition)
    ]
    shown = [s for s in scores if s.visible]

    overall = weighted(shown)
    by_category: dict[str, list[MetricScore]] = {}
    for s in shown:
        by_category.setdefault(s.definition.category, []).append(s)
    categories = []
    for category, members in sorted(by_category.items()):
        result = weighted(members)
        if result is not None:
            value, slo_min, slo, count = result
            categories.append(
                CategoryScore(category, value, rate(value, slo_min, slo), count)
            )

    return Summary(
        overall=overall[0] if overall else None,
        status_counts={
            status: sum(s.score.status == status for s in scores) for status in STATUSES
        },
        categories=categories,
    )
