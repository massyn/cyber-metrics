"""Dashboard pages: the metric scorecard, its per-metric scores and summary, and each metric's detail."""

from __future__ import annotations

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug.wrappers import Response

from scoring.detail import DetailFilters, build_detail
from scoring.scorecard import (
    ALL,
    STATUSES,
    ScorecardFilters,
    build_page,
    build_summary,
    score_metric,
)
from scoring.store import MetricStore

bp = Blueprint("dashboard", __name__)


def store() -> MetricStore:
    return current_app.extensions["metric_store"]


@bp.get("/")
def scorecard() -> str:
    """Renders straight away from the definitions; the browser then loads each metric's score."""
    filters = ScorecardFilters.from_args(request.args)
    page = build_page(store().definitions(), filters)
    return render_template(
        "scorecard.html", page=page, filters=filters, statuses=STATUSES, all_status=ALL
    )


@bp.get("/scores/<metric_id>")
def metric_score(metric_id: str) -> Response:
    """One metric's score, running its queries if they aren't cached."""
    run = store().run(metric_id)
    if run is None:
        abort(404)
    result = score_metric(run, ScorecardFilters.from_args(request.args))
    return jsonify(
        metric_id=metric_id,
        total=result.score.total,
        passed=result.score.passed,
        value=result.score.value,
        status=result.score.status,
        note=result.note,
        has_errors=bool(result.errors),
        visible=result.visible,
    )


@bp.get("/summary")
def summary() -> str:
    """Status counts, overall score and category scores, once every metric has run."""
    filters = ScorecardFilters.from_args(request.args)
    return render_template(
        "_summary.html",
        summary=build_summary(store().runs(), filters),
        filters=filters,
        statuses=STATUSES,
    )


@bp.get("/metric/<metric_id>")
def metric(metric_id: str) -> str | Response:
    run = store().run(metric_id)
    if run is None:
        flash(f"There is no metric called '{metric_id}'.", "warning")
        return redirect(url_for(".scorecard"))
    filters = DetailFilters.from_args(request.args)
    page = build_detail(run, filters, current_app.config["PAGE_SIZE"])
    return render_template("metric.html", page=page, filters=filters)
