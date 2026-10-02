"""Load metric definitions from the metric_*.yml files."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = (
    "metric_id",
    "title",
    "category",
    "type",
    "description",
    "weight",
    "indicator",
)


class DefinitionError(ValueError):
    """A metric definition file is missing a field or is malformed."""


@dataclass(frozen=True)
class MetricDefinition:
    metric_id: str
    title: str
    category: str
    type: str
    description: str
    how: str
    weight: float
    indicator: bool
    enabled: bool
    slo_min: float | None
    slo: float | None
    references: dict[str, list[str]]
    queries: tuple[str, ...]
    source_file: str


def parse_definition(raw: dict[str, Any], source_file: str) -> MetricDefinition:
    """Build a MetricDefinition from a parsed metric YAML document."""
    missing = [name for name in REQUIRED_FIELDS if name not in raw]
    if missing:
        raise DefinitionError(f"{source_file}: missing {', '.join(missing)}")

    # slo is [minimum, target]; a single value is used for both
    slo = raw.get("slo")
    if isinstance(slo, list):
        slo_min, slo_target = (slo[0], slo[-1]) if slo else (None, None)
    else:
        slo_min = slo_target = slo

    queries = raw.get("query") or []
    if isinstance(queries, str):
        raise DefinitionError(
            f"{source_file}: query must be a list of SQL strings, not a single string"
        )

    return MetricDefinition(
        metric_id=str(raw["metric_id"]),
        title=str(raw["title"]),
        category=str(raw["category"]),
        type=str(raw["type"]),
        description=str(raw["description"]).strip(),
        how=str(raw.get("how") or "").strip(),
        weight=float(raw["weight"]),
        indicator=bool(raw["indicator"]),
        enabled=bool(raw.get("enabled", True)),
        slo_min=None if slo_min is None else float(slo_min),
        slo=None if slo_target is None else float(slo_target),
        references={
            str(framework): [str(ref) for ref in refs or []]
            for framework, refs in (raw.get("references") or {}).items()
        },
        queries=tuple(queries),
        source_file=source_file,
    )


def load_definitions(directory: Path) -> list[MetricDefinition]:
    """Load every metric_*.yml in a directory, skipping (and logging) files that are invalid."""
    definitions = []
    for path in sorted(directory.glob("metric_*.yml")):
        try:
            with path.open(encoding="utf-8") as handle:
                definitions.append(parse_definition(yaml.safe_load(handle), path.name))
        except (OSError, yaml.YAMLError, DefinitionError, TypeError, ValueError):
            logger.exception("Skipping invalid metric definition %s", path.name)
    logger.info("Loaded %d metric definitions from %s", len(definitions), directory)
    return definitions
