"""Dashboard settings, read from the environment (or .env)."""

from __future__ import annotations

import os
import secrets
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Settings:
    metrics_path: Path
    data_path: Path
    page_size: int
    secret_key: str
    host: str
    port: int
    debug: bool

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            metrics_path=Path(
                os.environ.get("DASHBOARD_METRICS_PATH", REPO_ROOT / "02-metrics")
            ),
            data_path=Path(
                os.environ.get("METRICS_DATA", REPO_ROOT / "data" / "source")
            ),
            page_size=int(os.environ.get("DASHBOARD_PAGE_SIZE", "50")),
            # only signs flash messages, so a per-process random key is fine unless several workers share sessions
            secret_key=os.environ.get("DASHBOARD_SECRET_KEY") or secrets.token_hex(32),
            host=os.environ.get("DASHBOARD_HOST", "127.0.0.1"),
            port=int(os.environ.get("DASHBOARD_PORT", "5000")),
            debug=os.environ.get("DASHBOARD_DEBUG", "false").lower()
            in ("1", "true", "yes", "on"),
        )
