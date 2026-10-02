#!/bin/sh
# Collects the source data with posture, then starts the dashboard (03-dashboard), which runs the metrics.
# The exit status reports collection failures once the dashboard is stopped.
set -u
cd "$(dirname "$0")" || exit 1

status=0

# == collect (a failed source doesn't stop the run; the other tables are still written)
posturecollect --output "${POSTURE_OUTPUT:-data/source}" || status=1
posturecollect --include cve_db macadmins endoflife --output "${POSTURE_OUTPUT:-data/source}" || status=1

# == run the dashboard
cd 03-dashboard || exit 1
python ./app.py || status=1
exit $status
