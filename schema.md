# Data Sources Schema Documentation

This document describes all source tables, fields, and usage patterns for developing metrics in the cyber-metrics platform.

## Overview

The metrics system uses DuckDB with Jinja2 templating to query data sources. All data sources are referenced using the `{{ref('table_name')}}` pattern in YAML metric definitions.

## Data Source Tables

### **crowdstrike_hosts**
**Purpose**: Host/device inventory from CrowdStrike Falcon platform  
**Usage**: Used in 16 vulnerability management metrics

**Fields**:
- `device_id` (STRING) - Unique device identifier, used for joining with vulnerabilities
- `hostname` (STRING) - Hostname of the device  
- `last_seen` (STRING) - Last seen timestamp in format '%Y-%m-%dT%H:%M:%SZ'

**Example Usage**:
```sql
FROM {{ ref('crowdstrike_hosts') }} AS host
WHERE CURRENT_DATE - CAST(STRPTIME(host.last_seen, '%Y-%m-%dT%H:%M:%SZ') AS DATE) < 30
```

### **crowdstrike_vulnerabilities**
**Purpose**: Vulnerability data from CrowdStrike Falcon platform  
**Usage**: Used in 16 vulnerability management metrics

**Fields**:
- `aid` (STRING) - Asset ID, used for joining with hosts
- `status` (STRING) - Vulnerability status ('open', 'reopen', etc.)
- `severity` (STRING) - Vulnerability severity ('HIGH', 'CRITICAL', etc.)
- `published_date` (DATE) - CVE publication date
- `created_timestamp` (DATE) - Vulnerability creation timestamp
- `cve.id` (STRING) - CVE identifier
- `cve.remediation_level` (STRING) - Remediation level ('O' for official patch available)
- `cve.exploit_status` (INTEGER) - Exploit status (>0 indicates exploitable)
- `remediation.entities` (ARRAY) - Remediation information with title field

**Example Usage**:
```sql
FROM {{ ref('crowdstrike_vulnerabilities') }} AS cve
WHERE cve.status IN ('open', 'reopen')
  AND cve.severity IN ('HIGH', 'CRITICAL')
  AND coalesce(cve.cve.remediation_level = 'O', false)
  AND coalesce(cve.cve.exploit_status > 0, false)
```

### **tenable_assets**
**Purpose**: Asset inventory from Tenable.io vulnerability scanner  
**Usage**: Used in 10 vulnerability management metrics

**Fields**:
- `uuid` (STRING) - Unique asset identifier, used for joining with vulnerabilities
- `hostname` (STRING) - Hostname of the asset
- `last_seen` (DATE) - Last seen date

**Example Usage**:
```sql
FROM {{ ref('tenable_assets') }} AS asset
WHERE CURRENT_DATE - CAST(asset.last_seen AS DATE) < 30
```

### **tenable_vulnerabilities**
**Purpose**: Vulnerability data from Tenable.io vulnerability scanner  
**Usage**: Used in 10 vulnerability management metrics

**Fields**:
- `asset.uuid` (STRING) - Asset UUID for joining with assets
- `asset.hostname` (STRING) - Asset hostname
- `state` (STRING) - Vulnerability state ('OPEN', 'REOPENED', etc.)
- `severity` (STRING) - Vulnerability severity ('high', 'critical', etc.)
- `first_found` (DATE) - Date vulnerability was first discovered
- `last_found` (DATE) - Date vulnerability was last found
- `plugin.id` (STRING) - Plugin/check identifier
- `plugin.name` (STRING) - Plugin/check name
- `plugin.publication_date` (DATE) - Plugin publication date
- `plugin.cve` (ARRAY) - Array of CVE identifiers
- `plugin.exploit_available` (BOOLEAN) - Whether exploit is available
- `plugin.has_patch` (BOOLEAN) - Whether patch is available

**Example Usage**:
```sql
FROM {{ ref('tenable_vulnerabilities') }} AS cve
WHERE cve.state IN ('OPEN', 'REOPENED')
  AND cve.severity IN ('high', 'critical')
  AND cve.plugin.exploit_available IS TRUE
  AND cve.plugin.has_patch IS TRUE
```

### **okta_users**
**Purpose**: User identity data from Okta identity provider  
**Usage**: Used in 4 identity management metrics

**Fields**:
- `profile.login` (STRING) - User login/email identifier
- `status` (STRING) - User account status ('ACTIVE', etc.)
- `last_login` (DATE) - Last login date
- `password_changed` (DATE) - Password last changed date

**Example Usage**:
```sql
FROM {{ ref('okta_users') }}
WHERE status = 'ACTIVE'
  AND datediff('day', cast(last_login as date), current_date()) < 90
```

### **snyk_projects**
**Purpose**: Project/repository data from Snyk security platform  
**Usage**: Used in 1 software development metric

**Fields**:
- `id` (STRING) - Unique project identifier, used for joining with issues
- `attributes.name` (STRING) - Project name
- `attributes.target_file` (STRING) - Target file being scanned

### **snyk_issues**
**Purpose**: Security issues/vulnerabilities from Snyk security platform  
**Usage**: Used in 1 software development metric

**Fields**:
- `relationships.scan_item.data.id` (STRING) - Project ID for joining with projects
- `attributes.status` (STRING) - Issue status ('open', etc.)
- `attributes.effective_severity_level` (STRING) - Severity level ('critical', 'high', etc.)

### **knowbe4_enrollments**
**Purpose**: Security awareness training enrollment data from KnowBe4  
**Usage**: Used in 1 user security metric

**Fields**:
- `user.email` (STRING) - User email for joining with Okta users
- `completion_date` (DATE) - Training completion date

### **domains**
**Purpose**: DNS domain registration and configuration data  
**Usage**: Used in 3 network security metrics

**Fields**:
- `domain` (STRING) - Domain name
- `expiration_date` (DATE) - Domain expiration date
- Additional fields for SPF and DMARC configuration

## Development Patterns

### **Join Patterns**
- **CrowdStrike**: Join hosts and vulnerabilities on `host.device_id = cve.aid`
- **Tenable**: Join assets and vulnerabilities on `asset.uuid = cve.asset.uuid`
- **Okta + KnowBe4**: Join users and training on `okta.profile.login = training.user.email`

### **Date Handling**
- **CrowdStrike**: Uses ISO 8601 strings, convert with `STRPTIME(date, '%Y-%m-%dT%H:%M:%SZ')`
- **Others**: Use native DATE types, convert with `CAST(field AS DATE)`

### **Filtering Active Resources**
Most metrics filter for recently active resources (typically 30 days):
```sql
WHERE CURRENT_DATE - CAST(last_seen AS DATE) < 30
```

### **Vulnerability Classification**
Vulnerabilities are classified by:
- **Severity**: 'HIGH'/'CRITICAL' (CrowdStrike) or 'high'/'critical' (Tenable)
- **Status**: 'open'/'reopen' (CrowdStrike) or 'OPEN'/'REOPENED' (Tenable)
- **Exploitable**: `cve.exploit_status > 0` (CS) or `plugin.exploit_available IS TRUE` (Tenable)
- **Patchable**: `cve.remediation_level = 'O'` (CS) or `plugin.has_patch IS TRUE` (Tenable)

## Required Output Schema

All metrics must return these standardized columns:
- `resource` (STRING) - The resource being measured (hostname, login, domain, etc.)
- `resource_type` (STRING) - Type of resource ('host', 'user', 'domain', etc.)
- `compliance` (INTEGER) - Binary compliance score (1 = compliant, 0 = non-compliant)
- `detail` (STRING) - Additional context or details about the measurement

## Example Metric Structure

```yaml
---
metric_id: example_metric
title: Example Metric Title
category: Category Name
type: control|risk|performance
description: |
  Detailed description of what this metric measures
slo:
  - 0.8   # Warning threshold
  - 0.95  # Critical threshold
weight: 0.5
enabled: true
indicator: false
references:
  "ISO 27001:2022":
    - A.8.8
  "CIS 8.1":
    - 7.5
query:
  - |
    SELECT
      hostname AS resource,
      'host' AS resource_type,
      CASE WHEN condition THEN 1 ELSE 0 END AS compliance,
      'Detail information' AS detail
    FROM {{ ref('source_table') }}
    WHERE active_filter_conditions
```