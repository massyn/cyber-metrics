# Security Metrics Engine

The metrics engine processes collected security data into meaningful compliance metrics using YAML-defined SQL queries. It supports complex aggregations, historical trending, and compliance framework mapping.

## Quick Start

```bash
cd 02-metrics
python metrics.py                    # Run all metrics
python metrics.py -dryrun           # Test run without updating targets
python metrics.py -metric vm_coverage # Test specific metric
```

## Architecture

### Core Components

- **`metrics.py`** - Main execution engine that processes all metric definitions
- **`metric_*.yml`** - YAML files defining individual security metrics
- **Query Engine** - DuckDB with Jinja2 templating for SQL queries
- **Output Generation** - Parquet files with compliance scores and metadata

### Data Flow

```
JSON Data → DuckDB → SQL Queries → Metric Results → Parquet Output
    ↓          ↓         ↓            ↓              ↓
Raw Security  In-Memory  Jinja2     Compliance    Historical
Data Files    Database   Templates   Scores        Data
```

## Metric Definition Structure

Metrics are defined in YAML files with the following structure:

```yaml
# metric_example.yml
metric_id: access_mfa
title: "Access Control - Multi-Factor Authentication"
category: "Identity Management"
description: "Measures MFA adoption across user accounts"
how: "Counts users with MFA enabled vs total users"
weight: 1.0
indicator: true
type: "compliance"
slo: 0.95      # Target threshold (95%)
slo_min: 0.90  # Minimum acceptable threshold (90%)

# Compliance framework mappings
iso27001: ["A.9.4.2", "A.9.4.3"]
cis8_1: ["5.3", "5.4"]  
nist_csf: ["PR.AC-1", "PR.AC-7"]
essential8: ["Essential Eight Control 5"]

# SQL query with Jinja2 templating
query: |
  SELECT
    resource,
    resource_type,
    CASE 
      WHEN mfa_enabled = true THEN 1 
      ELSE 0 
    END as compliance,
    detail
  FROM {{ref('okta_users')}}
  WHERE account_status = 'ACTIVE'
```

## Required Query Output

All metric queries must return these columns:

| Column | Type | Description |
|--------|------|-------------|
| `resource` | String | Unique identifier for the assessed resource |
| `resource_type` | String | Type of resource (user, host, application, etc.) |
| `compliance` | Number (0-1) | Compliance score (1=compliant, 0=non-compliant) |
| `detail` | String | Human-readable description of the finding |

## Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `-h` | Display help information | |
| `-dryrun` | Test mode - show results without updating targets | `python metrics.py -dryrun` |
| `-metric <id>` | Run specific metric only | `python metrics.py -metric access_mfa` |
| `-path <path>` | Specify metric YAML files directory | `python metrics.py -path ./custom/` |
| `-data <path>` | Specify data source directory | `python metrics.py -data ../data/source` |
| `-parquet <path>` | Output parquet file location | `python metrics.py -parquet ../output/metrics.parquet` |
| `-privacyoff` | Disable privacy masking of resource/detail columns | `python metrics.py -privacyoff` |

## Data Reference System

The metrics engine uses a `{{ref('table_name')}}` function to reference collected data:

```sql
-- Reference CrowdStrike device data
SELECT * FROM {{ref('crowdstrike_devices')}}

-- Reference Tenable vulnerability data  
SELECT * FROM {{ref('tenable_vulnerabilities')}}

-- Reference Okta user data
SELECT * FROM {{ref('okta_users')}}
```

### Available Data Tables

| Collector | Table Reference | Description |
|-----------|----------------|-------------|
| CrowdStrike | `{{ref('crowdstrike_devices')}}` | Endpoint device information |
| CrowdStrike | `{{ref('crowdstrike_vulnerabilities')}}` | Endpoint vulnerabilities |
| Tenable | `{{ref('tenable_assets')}}` | Network asset inventory |
| Tenable | `{{ref('tenable_vulnerabilities')}}` | Vulnerability scan results |
| Okta | `{{ref('okta_users')}}` | User account information |
| Okta | `{{ref('okta_applications')}}` | Application integrations |
| Snyk | `{{ref('snyk_projects')}}` | Code project vulnerabilities |

> **Complete reference**: See the Data Model section below for available tables and schemas.

## Example Metrics

### Simple Compliance Check
```yaml
metric_id: endpoint_encryption
title: "Endpoint Encryption Coverage"
category: "Data Protection"
slo: 0.98
slo_min: 0.95

query: |
  SELECT
    hostname as resource,
    'endpoint' as resource_type,
    CASE 
      WHEN disk_encryption_status = 'encrypted' THEN 1 
      ELSE 0 
    END as compliance,
    'Disk encryption: ' || disk_encryption_status as detail
  FROM {{ref('crowdstrike_devices')}}
```

### Complex Aggregation
```yaml
metric_id: vulnerability_remediation
title: "Critical Vulnerability Remediation"
category: "Vulnerability Management"
slo: 0.95
slo_min: 0.90

query: |
  SELECT
    asset_uuid as resource,
    'asset' as resource_type,
    CASE 
      WHEN days_open <= 30 THEN 1
      WHEN days_open <= 60 THEN 0.5
      ELSE 0
    END as compliance,
    'Critical vulnerability open for ' || days_open || ' days' as detail
  FROM {{ref('tenable_vulnerabilities')}}
  WHERE severity = 'Critical'
    AND state = 'Open'
```

### Multi-Source Query
```yaml
metric_id: privileged_account_mfa
title: "Privileged Account MFA Coverage" 
category: "Identity Management"
slo: 1.0
slo_min: 0.98

query: |
  WITH privileged_users AS (
    SELECT DISTINCT user_id 
    FROM {{ref('okta_users')}} 
    WHERE admin_roles IS NOT NULL
  ),
  mfa_status AS (
    SELECT 
      user_id,
      mfa_enabled
    FROM {{ref('okta_users')}}
  )
  SELECT
    p.user_id as resource,
    'privileged_user' as resource_type,
    CASE WHEN m.mfa_enabled THEN 1 ELSE 0 END as compliance,
    CASE 
      WHEN m.mfa_enabled THEN 'MFA enabled for privileged account'
      ELSE 'MFA NOT enabled for privileged account'
    END as detail
  FROM privileged_users p
  JOIN mfa_status m ON p.user_id = m.user_id
```

## Data Model

### Input Data Structure
Collectors provide JSON data with standardized metadata:
```json
{
  "data": [...],           // Raw extracted data
  "metadata": {
    "_tenancy": "company",         // TENANT environment variable
    "_upload_timestamp": "2024-07-15T14:30:45Z",
    "_upload_id": "uuid"           // Unique ID for this collection run
  }
}
```

### Metric Output Schema
Each metric query must return this exact structure:
```sql
SELECT
  resource,        -- string: Unique identifier of the resource being measured
  resource_type,   -- string: Type of resource (user, host, device, etc.)
  compliance,      -- float: Compliance state (0.0 to 1.0, where 1.0 = compliant)
  detail           -- string: Additional information for remediation
FROM {{ref('data_source')}}
```

## Output Format

The metrics engine generates two output files:

### Detail Parquet
Individual resource-level compliance records:
```
../data/detail.parquet
```

Contains all resource-level findings with compliance scores and evidence.

### Summary Parquet
Aggregated metrics by organizational dimensions:
```
../data/summary.parquet
```

Contains rolled-up compliance statistics grouped by metric, business unit, team, and location.

## Development

### Creating a New Metric

When defining a metric, start by figuring out what you are trying to measure. Dashboard metrics are always a percentage, with 100% being good, so define metrics to reflect this consistent view. This approach allows for proper data aggregation.

1. **Create YAML file**: `metric_yourmetric.yml`
2. **Define metadata**:
   ```yaml
   metric_id: your_metric
   title: "Your Metric Title"
   category: "Your Category"
   description: "What this metric measures"
   how: "How the metric is calculated"
   weight: 1.0
   slo: 0.95
   slo_min: 0.90
   enabled: true
   indicator: false  # true if not percentage-based
   ```

3. **Write SQL query**:
   ```yaml
   query: |
     SELECT
       resource_id as resource,
       'resource_type' as resource_type,
       compliance_calculation as compliance,
       description as detail
     FROM {{ref('data_source')}}
   ```

4. **Test metric**:
   ```bash
   python metrics.py -metric your_metric -dryrun
   ```

### Complete YAML Schema Reference

| Field | Type | Description | Valid Values |
|-------|------|-------------|--------------|
| `metric_id` | string | Unique identifier for the metric | Any alphanumeric string |
| `title` | string | Descriptive title for the metric | Any string |
| `category` | string | Category (e.g., Vulnerability Management) | Any string |
| `type` | string | Type of metric being measured | `performance`, `control`, `risk` |
| `description` | string | Detailed explanation of the metric | Any multiline string |
| `how` | string | Instructions on how to compute the metric | Any multiline string |
| `slo` | list[float] | Service Level Objectives (performance thresholds) | List of decimal values (e.g., `0.9`) |
| `weight` | integer | Weight in overall scoring system | Integer between 0 and 100 |
| `enabled` | boolean | Whether the metric is currently active | `true`, `false` |
| `indicator` | boolean | If true, not aggregated as percentage | `true`, `false` (default) |
| `references` | object | Standards and guidelines related to metric | Key-value pairs |
| `query` | list[string] | SQL query definitions | List of multiline strings |

### Required Query Output Schema

The query MUST return these columns:

| Field | Type | Description | Valid Values |
|-------|------|-------------|--------------|
| `resource` | string | Unique identifier for the resource | Any alphanumeric string |
| `compliance` | float | Compliance percentage between 0 and 1 | Decimal between 0 and 1 |
| `detail` | string | Additional detail for remediation | Any string |
| `resource_type` | string | Resource type for asset mapping | `host`, `device`, `user`, etc. |

The query can optionally return dimensions: `business_unit`, `team`, `location`.

### Compliance Framework Mapping

Map metrics to compliance frameworks:

```yaml
# ISO 27001 controls
iso27001: ["A.12.6.1", "A.16.1.4"]

# CIS Controls v8.1  
cis8_1: ["4.1", "4.2", "4.3"]

# NIST Cybersecurity Framework
nist_csf: ["PR.DS-1", "PR.DS-2"]

# Australian Essential 8
essential8: ["Essential Eight Control 1"]
```

### Advanced SQL Features

The metrics engine supports advanced DuckDB SQL features:

```sql
-- Window functions for trending
SELECT 
  resource,
  compliance,
  LAG(compliance, 1) OVER (PARTITION BY resource ORDER BY date) as prev_compliance
FROM {{ref('historical_data')}}

-- JSON extraction
SELECT 
  json_extract(metadata, '$.severity') as severity
FROM {{ref('vulnerability_data')}}

-- Array operations
SELECT 
  resource,
  list_contains(permissions, 'admin') as has_admin
FROM {{ref('user_permissions')}}
```

## Workflow Example

Typical end-to-end metrics workflow:

```bash
# 1. Collect data first (if needed)
cd ../01-collectors
python wrapper.py

# 2. Run metrics with testing
cd ../02-metrics
python metrics.py -dryrun           # Verify queries work
python metrics.py -metric vm_coverage # Test specific metric

# 3. Run full metrics generation
python metrics.py                   # Generate complete metrics

# 4. Publish results
cd ../03-publish
python publish.py                   # Send to dashboard
```

## Testing & Validation

### Dry Run Mode
Test metrics without updating targets:
```bash
python metrics.py -dryrun
```

Shows:
- SQL query execution results
- Compliance score calculations  
- Data validation errors
- Performance metrics

### Single Metric Testing
```bash
python metrics.py -metric access_mfa -dryrun
```

Displays:
- Full query results
- Compliance distribution
- Sample records
- Execution time

### Data Validation

The engine validates:
- **Required columns**: Ensures query returns `resource`, `resource_type`, `compliance`, `detail`
- **Data types**: Validates compliance scores are numeric (0-1)
- **Referential integrity**: Checks that referenced tables exist
- **Query syntax**: Validates SQL syntax before execution

## Performance Optimization

### Query Performance
- **Use indexes**: DuckDB automatically creates indexes for common patterns
- **Limit data scope**: Filter data early in queries
- **Avoid cartesian products**: Use proper JOIN conditions
- **Use CTEs**: Break complex queries into readable components

### Memory Management
- **Streaming processing**: Large datasets are processed in chunks
- **Columnar storage**: Parquet format provides efficient storage and querying
- **Garbage collection**: Automatic cleanup of temporary tables

## Monitoring

### Execution Metrics
Each metric run provides:
- **Execution time**: Query performance monitoring
- **Record counts**: Input and output record statistics
- **Error rates**: Failed queries and validation errors
- **Resource usage**: Memory and CPU utilization

### Logging
Structured logging includes:
- **Metric execution**: Start/end times, record counts
- **Query performance**: Execution time, optimization hints
- **Data quality**: Validation errors, missing data warnings
- **System health**: Resource usage, error rates

## Troubleshooting

### Common Issues

**No data found errors**: Ensure collectors have run and data exists in `../data/source/`

**SQL query errors**: Use `-dryrun` to test queries without side effects  

**Missing tables**: Verify collector names match `{{ref('table_name')}}` references in metric YAML files

**Performance issues**: Use query optimization techniques and check data volume

**Validation failures**: Ensure queries return required columns: `resource`, `resource_type`, `compliance`, `detail`

## Links

- **[Metric List](../00-docs/metrics.md)** - Complete catalog of available metrics