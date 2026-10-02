from __future__ import annotations

import textwrap
from pathlib import Path

import pandas as pd
import pytest
from flask import Flask

from app import create_app
from config import Settings


def write_metric(directory: Path, metric_id: str, body: str) -> None:
    (directory / f"metric_{metric_id}.yml").write_text(
        textwrap.dedent(body), encoding="utf-8"
    )


@pytest.fixture
def data_path(tmp_path: Path) -> Path:
    path = tmp_path / "source"
    path.mkdir()
    pd.DataFrame(
        {
            "hostname": ["web-1", "web-2", "db-1", "db-2"],
            "encrypted": [True, True, False, True],
            "owner": ["web", "web", "data", "data"],
        }
    ).to_parquet(path / "acme_hosts.parquet")
    pd.DataFrame({"login": ["alice", "bob"], "mfa": [True, False]}).to_parquet(
        path / "acme_users.parquet"
    )
    return path


@pytest.fixture
def metrics_path(tmp_path: Path) -> Path:
    path = tmp_path / "metrics"
    path.mkdir()
    write_metric(
        path,
        "dp_encryption",
        """
        metric_id: dp_encryption
        title: Encrypted hosts
        category: Data Protection
        type: control
        description: Hosts with encrypted disks.
        how: Check each host.
        weight: 1.0
        indicator: false
        slo: [0.5, 0.9]
        references:
          "CIS 8.1":
            - 3.6
        query:
          - |
            SELECT hostname AS resource, 'host' AS resource_type,
                   CASE WHEN encrypted THEN 1 ELSE 0 END AS compliance,
                   'encrypted: ' || encrypted AS detail, owner
            FROM {{ ref('acme_hosts') }}
        """,
    )
    write_metric(
        path,
        "im_mfa",
        """
        metric_id: im_mfa
        title: Users with MFA
        category: Identity Management
        type: risk
        description: Users with MFA.
        how: Check each user.
        weight: 3.0
        indicator: false
        slo: [0.9, 0.95]
        query:
          - |
            SELECT login AS resource, 'user' AS resource_type,
                   CASE WHEN mfa THEN 1 ELSE 0 END AS compliance, '' AS detail
            FROM {{ ref('acme_users') }}
          - |
            SELECT * FROM {{ ref('acme_missing') }}
        """,
    )
    write_metric(
        path,
        "ns_waf",
        """
        metric_id: ns_waf
        title: Web apps behind a WAF
        category: Network Security
        type: control
        description: Apps behind a WAF.
        how: Not implemented yet.
        weight: 1.0
        indicator: false
        slo: [0.9, 0.95]
        query: null
        """,
    )
    return path


@pytest.fixture
def app(metrics_path: Path, data_path: Path) -> Flask:
    settings = Settings(
        metrics_path=metrics_path,
        data_path=data_path,
        page_size=2,
        secret_key="test",
        host="127.0.0.1",
        port=5000,
        debug=False,
    )
    return create_app(settings)
