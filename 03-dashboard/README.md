# Metrics Dashboard

A Flask app that runs every metric in `02-metrics/` against posture's parquet files in `data/source/` and shows the current results. It keeps no history.

## Quick Start

```bash
pip install -r requirements.txt   # from the repo root
cd 03-dashboard
python app.py                      # http://127.0.0.1:5000
```

The scorecard page appears straight away. Your browser then loads each metric's score from its own endpoint, four at a time, so a slow query only holds up its own row. Each metric runs once and its result is kept in memory. Results are re-run automatically when any `metric_*.yml` or source parquet file changes.

## Pages

- **Scorecard** (`/`): every metric with its score, resource count and SLO, colour-coded green (meeting the SLO target), amber (below target but at or above the minimum) or red (below the minimum). Click a column heading to sort. Once every score has loaded, the summary shows the weighted overall score, how many metrics are in each status (click one to filter by it), and a weighted score for each category, rated against the weighted SLOs of its metrics. Indicator metrics are left out of the weighted scores. Filter by search text, category, type and status. Metrics with no data (disabled, no query yet, or every query failed) are hidden unless you pick **All metrics** or **No data**.
- **Metric detail** (`/metric/<metric_id>`): the metric's description, framework references, score and every resource row. Filter by compliance, resource type and search text. Sort by any column and page through the results. Query errors, such as a missing source table, are shown at the top.

## Configuration

Settings are read from the environment or a `.env` file.

| Variable | Default | Purpose |
|----------|---------|---------|
| `DASHBOARD_METRICS_PATH` | `<repo>/02-metrics` | Directory containing the `metric_*.yml` files |
| `METRICS_DATA` | `<repo>/data/source` | Directory containing posture's parquet files |
| `DASHBOARD_PAGE_SIZE` | `50` | Rows per page on the detail page |
| `DASHBOARD_HOST` | `127.0.0.1` | Address to listen on |
| `DASHBOARD_PORT` | `5000` | Port to listen on |
| `DASHBOARD_DEBUG` | `false` | Flask debug mode |
| `DASHBOARD_SECRET_KEY` | random per process | Signs flash messages. Set it if you run several workers |

## Layout

| Path | Purpose |
|------|---------|
| `app.py` | Entry point: builds the Flask app |
| `config.py` | Settings from the environment |
| `engine/definitions.py` | Loads and validates `metric_*.yml` files |
| `engine/runner.py` | Resolves `{{ ref('table') }}` to the latest parquet snapshot and runs each query in DuckDB |
| `scoring/store.py` | Loads definitions, and runs each metric on demand, caching the result until a file changes |
| `scoring/scorecard.py` | Scores metrics against their SLO, and the weighted overall and category scores |
| `scoring/detail.py` | Filters, sorts and pages a metric's resource rows |
| `web/routes.py` | The scorecard and detail pages, the per-metric score endpoint (`/scores/<metric_id>`) and the summary (`/summary`) |
| `templates/`, `static/` | Bootstrap 5 templates, styles and a little JavaScript |

## Tests

```bash
cd 03-dashboard
python -m pytest
```
