"""Build a metric's detail page: its score and the filtered, sorted, paged resource rows."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from engine.definitions import MetricDefinition
from engine.runner import MetricRun
from scoring.scorecard import Score, score

PASS, FAIL = "pass", "fail"
SORTABLE = ("resource", "resource_type", "compliance", "detail")


@dataclass(frozen=True)
class DetailFilters:
    compliance: str = ""  # "", PASS or FAIL
    resource_type: str = ""
    search: str = ""
    sort: str = "compliance"
    descending: bool = False
    page: int = 1

    @classmethod
    def from_args(cls, args: Mapping[str, str]) -> DetailFilters:
        compliance = args.get("compliance", "")
        sort = args.get("sort", "compliance")
        page = args.get("page", "1")
        return cls(
            compliance=compliance if compliance in (PASS, FAIL) else "",
            resource_type=args.get("resource_type", ""),
            search=args.get("search", "").strip(),
            sort=sort if sort in SORTABLE else "compliance",
            descending=args.get("order") == "desc",
            page=int(page) if page.isdigit() and int(page) > 0 else 1,
        )

    def as_args(self, **overrides: Any) -> dict[str, Any]:
        """The active filters as URL arguments, with any overrides (e.g. a different page or sort)."""
        args = {
            "compliance": self.compliance,
            "resource_type": self.resource_type,
            "search": self.search,
            "sort": self.sort,
            "order": "desc" if self.descending else "asc",
            "page": self.page,
            **overrides,
        }
        return {key: value for key, value in args.items() if value not in ("", None)}


@dataclass(frozen=True)
class DetailPage:
    definition: MetricDefinition
    errors: list[str]
    score: Score
    records: list[dict[str, Any]]
    matching_records: int
    page: int
    pages: int
    resource_types: list[str]


def build_detail(run: MetricRun, filters: DetailFilters, page_size: int) -> DetailPage:
    # the score covers every resource, whatever the page's filters, so it matches the scorecard
    detail = run.detail
    metric_score = score(run.definition, detail)
    resource_types = sorted(detail["resource_type"].unique())

    if filters.compliance == PASS:
        detail = detail[detail["compliance"] >= 1]
    elif filters.compliance == FAIL:
        detail = detail[detail["compliance"] < 1]
    if filters.resource_type:
        detail = detail[detail["resource_type"] == filters.resource_type]
    if filters.search:
        needle = filters.search.lower()
        detail = detail[
            detail["resource"].str.lower().str.contains(needle, regex=False)
            | detail["detail"].str.lower().str.contains(needle, regex=False)
        ]

    detail = detail.sort_values(
        [filters.sort, "resource"],
        ascending=[not filters.descending, True],
        kind="stable",
    )
    pages = max(1, math.ceil(len(detail) / page_size))
    page = min(filters.page, pages)
    window = detail.iloc[(page - 1) * page_size : page * page_size].copy()
    window["outcome"] = window["compliance"].map(
        lambda value: PASS if value >= 1 else FAIL if value <= 0 else "partial"
    )

    return DetailPage(
        definition=run.definition,
        errors=run.errors,
        score=metric_score,
        records=window.to_dict("records"),
        matching_records=len(detail),
        page=page,
        pages=pages,
        resource_types=resource_types,
    )
