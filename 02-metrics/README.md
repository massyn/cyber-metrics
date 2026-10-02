# Metric Definitions

Each `metric_*.yml` file in this folder defines one security metric: its metadata, its SLO, the compliance controls it maps to, and the SQL queries that score every resource. The [dashboard](../03-dashboard/) runs these queries against posture's parquet files and shows the results.

## Quick Start

```bash
cd ../03-dashboard
python app.py        # runs every metric and serves the results at http://127.0.0.1:5000
```

## How Metrics Are Run

- **`metric_*.yml`** - one file per metric, in this folder
- **Engine** - `03-dashboard/engine/` loads the definitions, points each `{{ref('...')}}` at the latest parquet file, and runs the queries in DuckDB
- **Results** - each metric's score (compliant ÷ total) and resource-level detail, shown on the dashboard

```
Parquet Data → DuckDB → SQL Queries → Metric Results → Dashboard
     ↓            ↓          ↓              ↓
posturecollect  In-Memory  Jinja2      Compliance
output          Engine     Templates   Scores
```

## Metric Definition Structure

Metrics are defined in YAML files with the following structure:

```yaml
# metric_im_privileged_mfa.yml
metric_id: im_privileged_mfa
title: "Privileged accounts with MFA"
category: "Identity Management"
type: control
description: |
  The percentage of active privileged accounts with at least one active MFA factor.
how: |
  Find all active Okta users holding an admin role, and check whether each has an active MFA factor.
weight: 1.0
slo:
  - 0.90  # Minimum acceptable threshold (90%)
  - 0.95  # Target threshold (95%)
enabled: true
indicator: false

# Compliance framework mappings (framework names and refs as listed in 99-templates/framework.csv)
references:
  "ISO 27001:2022":
    - A.8.5
  "CIS 8.1":
    - 6.5
  "NIST CSF v2.0":
    - PR.AA-03

# One or more SQL queries; their results are combined
query:
  - |
    SELECT
      users.profile_login AS resource,
      'user' AS resource_type,
      CASE WHEN count(factors.id) > 0 THEN 1 ELSE 0 END AS compliance,
      CAST(count(factors.id) AS VARCHAR) || ' active MFA factors' AS detail
    FROM {{ref('okta_users')}} AS users
    JOIN (SELECT DISTINCT user_id FROM {{ref('okta_user_roles')}}) AS admins
      ON admins.user_id = users.id
    LEFT JOIN {{ref('okta_user_factors')}} AS factors
      ON factors.user_id = users.id
      AND factors.status = 'ACTIVE'
    WHERE users.status = 'ACTIVE'
    GROUP BY users.profile_login
```

## Required Query Output

All metric queries must return these columns:

| Column | Type | Description |
|--------|------|-------------|
| `resource` | String | Unique identifier for the assessed resource |
| `resource_type` | String | Type of resource (user, host, application, etc.) |
| `compliance` | Number (0-1) | Compliance score (1=compliant, 0=non-compliant) |
| `detail` | String | Human-readable description of the finding |

## Data Reference System

The metrics engine uses a `{{ref('table_name')}}` function to reference collected data. Table names follow posture's `<source>_<resource>` naming:

```sql
-- Reference CrowdStrike host data
SELECT * FROM {{ref('crowdstrike_hosts')}}

-- Reference Tenable.io vulnerability data
SELECT * FROM {{ref('tenableio_vulnerabilities')}}

-- Reference Okta user data
SELECT * FROM {{ref('okta_users')}}
```

If a referenced table has no parquet file, that query is skipped and the error is shown on the metric's dashboard page.

### Tables Used by the Current Metrics

| Source | Table Reference | Description |
|--------|----------------|-------------|
| CrowdStrike | `{{ref('crowdstrike_hosts')}}` | Endpoint hosts with the Falcon sensor |
| CrowdStrike | `{{ref('crowdstrike_vulnerabilities')}}` | Open endpoint vulnerabilities |
| CrowdStrike | `{{ref('crowdstrike_vulnerability_remediations')}}` | Remediation steps per vulnerability (join on `id`) |
| Tenable.io | `{{ref('tenableio_assets')}}` | Scanned asset inventory |
| Tenable.io | `{{ref('tenableio_vulnerabilities')}}` | Vulnerability findings |
| cve-db | `{{ref('cve_db_cve_summary')}}` | NVD data per CVE, used to classify vulnerabilities as OS or application |
| Kandji | `{{ref('kandji_devices')}}` | Managed Macs and Windows devices, with check-in status |
| Kandji | `{{ref('kandji_device_details')}}` | Device detail, including macOS version and FileVault status |
| Workspace ONE | `{{ref('workspaceone_computers')}}` | Managed computers, with enrolment status |
| Salesforce | `{{ref('salesforce_fixed_asset__c')}}` | Asset register (serial numbers) |
| Salesforce | `{{ref('salesforce_krow__project_resources__c')}}` | Staff records, including employment end dates |
| endoflife.date | `{{ref('endoflife_cycles')}}` | Support status of each product release cycle |
| macadmins.io | `{{ref('macadmins_macos_cves')}}` | CVEs fixed in each macOS release, and whether they were exploited |
| Okta | `{{ref('okta_users')}}` | User accounts |
| Okta | `{{ref('okta_user_factors')}}` | Enrolled MFA factors per user |
| Okta | `{{ref('okta_devices')}}` | Registered devices, including disk encryption |
| KnowBe4 | `{{ref('knowbe4_training_enrollments')}}` | Security awareness training enrolments |
| KnowBe4 | `{{ref('knowbe4_pst_recipients')}}` | Simulated phishing results per recipient |
| Cloudflare | `{{ref('cloudflare_zones')}}` | DNS zones hosted in Cloudflare |
| Cloudflare | `{{ref('cloudflare_dns_records')}}` | DNS records, including whether they're proxied |
| DNSimple | `{{ref('dnsimple_domains')}}` | Registered domains and their expiry |
| DNSimple | `{{ref('dnsimple_zone_records')}}` | DNS records for DNSimple-hosted zones |
| GitHub | `{{ref('github_repositories')}}` | Repositories (archived ones are excluded) |
| GitHub | `{{ref('github_dependabot_alerts')}}` | Open Dependabot alerts |
| Snyk | `{{ref('snyk_projects')}}` | Code projects |
| Snyk | `{{ref('snyk_issues')}}` | Issues per project (join on `project_id`) |

> **Complete reference**: [schema.md](../schema.md) covers the fields the current metrics use. Every table posture can collect, with its columns, is listed in [posture's docs](https://github.com/massyn/posture/blob/main/docs/index.md).

## Example Metrics

These examples show only the fields that shape the query. A real metric file also needs the other required fields shown in [Metric Definition Structure](#metric-definition-structure).

### Simple Compliance Check
```yaml
metric_id: endpoint_full_functionality
title: "Endpoint Sensors in Full Functionality Mode"
category: "Malware Protection"
slo:
  - 0.95
  - 0.98

query:
  - |
    SELECT
      hostname AS resource,
      'host' AS resource_type,
      CASE
        WHEN reduced_functionality_mode IS TRUE THEN 0
        ELSE 1
      END AS compliance,
      'Reduced functionality mode: ' || coalesce(CAST(reduced_functionality_mode AS VARCHAR), 'unknown') AS detail
    FROM {{ref('crowdstrike_hosts')}}
    WHERE CURRENT_DATE - CAST(last_seen AS DATE) < 30
```

### Complex Aggregation
```yaml
metric_id: vulnerability_remediation
title: "Critical Vulnerability Remediation"
category: "Vulnerability Management"
slo:
  - 0.90
  - 0.95

query:
  - |
    SELECT
      asset_hostname AS resource,
      'host' AS resource_type,
      CASE
        WHEN date_diff('day', CAST(first_found AS DATE), CURRENT_DATE) <= 30 THEN 1
        ELSE 0
      END AS compliance,
      plugin_name || ' open for ' || date_diff('day', CAST(first_found AS DATE), CURRENT_DATE) || ' days' AS detail
    FROM {{ref('tenableio_vulnerabilities')}}
    WHERE severity = 'critical'
      AND state IN ('OPEN', 'REOPENED')
```

### Multi-Source Query
```yaml
metric_id: privileged_account_mfa
title: "Privileged Account MFA Coverage"
category: "Identity Management"
slo:
  - 0.98
  - 1.0

query:
  - |
    WITH privileged_users AS (
      SELECT DISTINCT user_id
      FROM {{ref('okta_user_roles')}}
    ),
    mfa_users AS (
      SELECT DISTINCT user_id
      FROM {{ref('okta_user_factors')}}
      WHERE status = 'ACTIVE'
    )
    SELECT
      u.profile_login AS resource,
      'user' AS resource_type,
      CASE WHEN m.user_id IS NOT NULL THEN 1 ELSE 0 END AS compliance,
      CASE
        WHEN m.user_id IS NOT NULL THEN 'MFA enabled for privileged account'
        ELSE 'MFA NOT enabled for privileged account'
      END AS detail
    FROM {{ref('okta_users')}} u
    JOIN privileged_users p ON p.user_id = u.id
    LEFT JOIN mfa_users m ON m.user_id = u.id
    WHERE u.status = 'ACTIVE'
```

## Data Model

### Input Data Structure
Source data comes from [posture](https://github.com/massyn/posture)'s `posturecollect`, which writes one Parquet file per table to the data path (default `../data/source`):

```
data/source/<source>_<resource>.parquet                 # default: latest snapshot, overwritten each run
data/source/<source>_<resource>/<YYYY.MM.DD>.parquet    # with --history: one snapshot per day
```

`{{ref('<source>_<resource>')}}` resolves to the matching file. With `--history`, only the most recent snapshot is read.

Each file is one flat table. Columns are typed as posture declares them (strings, numbers, timestamps, etc.), so no casting from text is needed. Every table also has a metadata column:

| Column | Type | Description |
|--------|------|-------------|
| `_collected_at` | `TIMESTAMP WITH TIME ZONE` | UTC time the data was collected |

For example, `endoflife_products`:

| Column | Type |
|--------|------|
| `product` | `VARCHAR` |
| `label` | `VARCHAR` |
| `category` | `VARCHAR` |
| `aliases` | `VARCHAR` |
| `tags` | `VARCHAR` |
| `uri` | `VARCHAR` |
| `_collected_at` | `TIMESTAMP WITH TIME ZONE` |

See [posture's docs](https://github.com/massyn/posture/blob/main/docs/index.md) for the tables and column types for every source.

### Metric Output Schema
Each metric query must return this exact structure:
```sql
SELECT
  resource,        -- string: Unique identifier of the resource being measured
  resource_type,   -- string: Type of resource (user, host, device, etc.)
  compliance,      -- float: Compliance state (0.0 to 1.0, where 1.0 = compliant)
  detail           -- string: Additional information for remediation
FROM {{ref('<source>_<resource>')}}
```

`detail` must be text. Cast timestamps and numbers with `CAST(... AS VARCHAR)` before using them as `detail`.

## Development

### Creating a New Metric

When defining a metric, start by figuring out what you are trying to measure. Dashboard metrics are always a percentage, with 100% being good, so define metrics to reflect this consistent view. This approach allows for proper data aggregation.

1. **Create YAML file**: `metric_yourmetric.yml`
2. **Define metadata**:
   ```yaml
   metric_id: your_metric
   title: "Your Metric Title"
   category: "Your Category"
   type: control
   description: "What this metric measures"
   how: "How the metric is calculated"
   weight: 1.0
   slo:
     - 0.90  # minimum acceptable
     - 0.95  # target
   enabled: true
   indicator: false  # true if not percentage-based
   references:
     "ISO 27001:2022":
       - A.8.8
   ```

3. **Write SQL query**:
   ```yaml
   query:
     - |
       SELECT
         hostname AS resource,
         'host' AS resource_type,
         CASE WHEN <condition> THEN 1 ELSE 0 END AS compliance,
         <description> AS detail
       FROM {{ref('<source>_<resource>')}}
   ```

4. **Test metric**: open `http://127.0.0.1:5000/metric/your_metric` on the running dashboard. It picks up the new file automatically, and any query errors are shown at the top of the page.

### Complete YAML Schema Reference

| Field | Type | Description | Valid Values |
|-------|------|-------------|--------------|
| `metric_id` | string | Unique identifier for the metric, used in the dashboard and docs URLs | Lowercase letters, digits and `_`; usually matches the file name `metric_<metric_id>.yml` |
| `title` | string | Descriptive title for the metric | Any string |
| `category` | string | Category (e.g., Vulnerability Management) | One of the categories in `generate_documentation.py` |
| `type` | string | Type of metric being measured | `performance`, `control`, `risk` |
| `description` | string | Detailed explanation of the metric | Any multiline string |
| `how` | string | Instructions on how to compute the metric (optional) | Any multiline string |
| `slo` | list[float] | Service Level Objectives: `[minimum, target]` | Two decimal values, e.g. `[0.90, 0.95]` |
| `weight` | float | Weight in overall scoring system | Decimal between 0 and 1, e.g. `0.8` |
| `enabled` | boolean | Whether the metric's queries are run | `true` (default), `false` |
| `indicator` | boolean | If true, left out of the dashboard's weighted overall score | `true`, `false` |
| `references` | object | Compliance frameworks, each with a list of control refs | See below |
| `query` | list[string] | SQL queries; results from every query are combined | List of multiline strings, or `null` for a metric with no query yet |

### Required Query Output Schema

The query MUST return these columns:

| Field | Type | Description | Valid Values |
|-------|------|-------------|--------------|
| `resource` | string | Unique identifier for the resource | Any alphanumeric string |
| `compliance` | float | Compliance percentage between 0 and 1 | Decimal between 0 and 1 |
| `detail` | string | Additional detail for remediation | Any string |
| `resource_type` | string | Resource type for asset mapping | `host`, `device`, `user`, etc. |

Any other columns a query returns are ignored.

### Compliance Framework Mapping

Map metrics to compliance frameworks under `references`. Framework names and refs must match `99-templates/framework.csv`, which `generate_documentation.py` uses to link each ref to its control:

```yaml
references:
  "ISO 27001:2022":
    - A.8.8
  "CIS 8.1":
    - 7.5
    - 7.6
  "NIST CSF v2.0":
    - ID.RA-01
  "Essential8":
    - ISM-1698
```

### Useful DuckDB SQL Features

```sql
-- Date arithmetic on posture's typed timestamps
SELECT hostname, CURRENT_DATE - CAST(last_seen AS DATE) AS days_since_seen
FROM {{ref('crowdstrike_hosts')}}

-- JSON array columns (posture stores these as JSON text)
SELECT asset_hostname, unnest(from_json(cve, '["VARCHAR"]')) AS cve_id
FROM {{ref('tenableio_vulnerabilities')}}

-- Array membership
SELECT asset_hostname, plugin_name
FROM {{ref('tenableio_vulnerabilities')}}
WHERE list_contains(from_json(cve, '["VARCHAR"]'), 'CVE-2024-3094')
```

## Workflow Example

Typical end-to-end workflow:

```bash
# 1. Collect data (from the repo root)
posturecollect --output data/source

# 2. Run the metrics and view the results
cd 03-dashboard
python app.py
```

## Testing & Validation

### Testing a Metric

Open the metric on the dashboard (`/metric/<metric_id>`). The page shows its score, every resource row, and any query errors. The dashboard re-runs the metrics whenever a `metric_*.yml` or source parquet file changes, so edit the file and refresh the page.

### Data Validation

When loading definitions, the engine checks:
- **Metadata**: the YAML has `metric_id`, `title`, `category`, `type`, `description`, `weight` and `indicator` (`how` is optional), and `query` is a list. Invalid files are skipped and logged

For each query, it checks:
- **Referenced tables**: every `{{ref('...')}}` table has a parquet file; if not, the query is skipped
- **Query execution**: a query that DuckDB rejects is skipped, with DuckDB's error shown
- **Required columns**: the result includes `resource`, `resource_type`, `compliance` and `detail`
- **Compliance values**: rows whose `compliance` isn't numeric are dropped and reported

A metric whose queries all return nothing is listed under the **No data** status on the scorecard.

## Logging

The dashboard logs each skipped query with the reason, and how long each full run of the metrics took.

## Troubleshooting

### Common Issues

**Source table not found**: Run `posturecollect` (see `../01-collectors`) and check the parquet file is in `data/source/`, or in the folder set by `METRICS_DATA`

**SQL query errors**: Open the metric on the dashboard; DuckDB's error message is shown at the top of the page

**Missing tables**: `{{ref('...')}}` names must match posture's `<source>_<resource>` file names. Sources that need no credentials, such as `cve_db`, are only collected when named with `posturecollect --include`

**Validation failures**: Ensure queries return required columns: `resource`, `resource_type`, `compliance`, `detail`

## Links

- **[Metric List](../00-docs/metrics.md)** - Complete catalog of available metrics
