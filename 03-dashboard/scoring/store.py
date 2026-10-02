"""Load metric definitions, and run each metric on demand, caching the result until a source file changes."""

from __future__ import annotations

import logging
import threading
import time
from pathlib import Path

from engine.definitions import MetricDefinition, load_definitions
from engine.runner import MetricRun, run_metric

logger = logging.getLogger(__name__)


class MetricStore:
    def __init__(self, metrics_path: Path, data_path: Path) -> None:
        self.metrics_path = metrics_path
        self.data_path = data_path
        self._lock = threading.Lock()
        self._metric_locks: dict[str, threading.Lock] = {}
        self._signature: tuple[tuple[str, int, int], ...] | None = None
        self._generation = 0
        self._definitions: dict[str, MetricDefinition] = {}
        self._runs: dict[str, MetricRun] = {}

    def _refresh(self) -> int:
        """Reload definitions and drop cached results if any metric_*.yml or source parquet file has changed."""
        files = [
            *self.metrics_path.glob("metric_*.yml"),
            *self.data_path.rglob("*.parquet"),
        ]
        signature = tuple(
            sorted((str(p), p.stat().st_mtime_ns, p.stat().st_size) for p in files)
        )
        with self._lock:
            if signature != self._signature:
                self._definitions = {
                    d.metric_id: d for d in load_definitions(self.metrics_path)
                }
                self._runs = {}
                self._signature = signature
                self._generation += 1
            return self._generation

    def definitions(self) -> list[MetricDefinition]:
        self._refresh()
        with self._lock:
            return list(self._definitions.values())

    def cached_runs(self) -> list[MetricRun]:
        """Results already computed, without running anything."""
        self._refresh()
        with self._lock:
            return list(self._runs.values())

    def run(self, metric_id: str) -> MetricRun | None:
        """One metric's results, running its queries only if they aren't cached.

        Different metrics run in parallel; concurrent requests for the same metric wait for one run.
        """
        generation = self._refresh()
        with self._lock:
            definition = self._definitions.get(metric_id)
            cached = self._runs.get(metric_id)
            metric_lock = self._metric_locks.setdefault(metric_id, threading.Lock())
        if definition is None or cached is not None:
            return cached

        with metric_lock:
            with self._lock:
                cached = self._runs.get(metric_id)
            if cached is not None:
                return cached
            started = time.perf_counter()
            result = run_metric(definition, self.data_path)
            logger.info(
                "Ran metric %s in %.1fs", metric_id, time.perf_counter() - started
            )
            with self._lock:
                # don't cache a result computed from files that changed while it ran
                if generation == self._generation:
                    self._runs[metric_id] = result
            return result

    def runs(self) -> list[MetricRun]:
        """Results for every metric, running any that aren't cached."""
        return [
            run
            for definition in self.definitions()
            if (run := self.run(definition.metric_id)) is not None
        ]
