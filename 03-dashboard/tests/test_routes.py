from __future__ import annotations

from flask import Flask


def test_scorecard_renders_without_running_metrics(app: Flask) -> None:
    response = app.test_client().get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Encrypted hosts" in html and "Users with MFA" in html
    assert "/scores/dp_encryption" in html
    assert app.extensions["metric_store"].cached_runs() == []


def test_score_endpoint_returns_json(app: Flask) -> None:
    result = app.test_client().get("/scores/dp_encryption").get_json()
    assert result == {
        "metric_id": "dp_encryption",
        "total": 4,
        "passed": 3.0,
        "value": 0.75,
        "status": "warning",
        "note": "",
        "has_errors": False,
        "visible": True,
    }


def test_score_endpoint_applies_the_status_filter(app: Flask) -> None:
    client = app.test_client()
    assert client.get("/scores/ns_waf").get_json()["visible"] is False
    assert client.get("/scores/ns_waf?status=all").get_json()["visible"] is True
    assert client.get("/scores/im_mfa").get_json()["has_errors"] is True


def test_score_endpoint_unknown_metric(app: Flask) -> None:
    assert app.test_client().get("/scores/nope").status_code == 404


def test_summary_shows_counts_and_category_scores(app: Flask) -> None:
    html = app.test_client().get("/summary").get_data(as_text=True)
    assert "Score by category" in html
    assert "Data Protection" in html and "75.0%" in html
    assert "56.2%" in html  # overall: (0.75 * 1 + 0.5 * 3) / 4


def test_metric_detail_page(app: Flask) -> None:
    response = app.test_client().get("/metric/dp_encryption?compliance=fail")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "db-1" in html and "web-1" not in html
    assert "CIS 8.1" in html


def test_metric_detail_shows_query_errors(app: Flask) -> None:
    html = app.test_client().get("/metric/im_mfa").get_data(as_text=True)
    assert "acme_missing" in html


def test_metric_detail_paginates(app: Flask) -> None:
    html = app.test_client().get("/metric/dp_encryption?page=2").get_data(as_text=True)
    assert "Page 2 of 2" in html


def test_unknown_metric_redirects_with_message(app: Flask) -> None:
    response = app.test_client().get("/metric/nope", follow_redirects=True)
    assert response.status_code == 200
    assert "There is no metric called" in response.get_data(as_text=True)
