# Data Sources Schema Documentation

This document describes the source tables, fields, and usage patterns used by the current metrics in the cyber-metrics platform.

## Overview

Source data is collected by [posture](https://github.com/massyn/posture)'s `posturecollect` (see `01-collectors/`), which writes one Parquet file per table. The metrics system uses DuckDB with Jinja2 templating to query them. Tables are referenced with the `{{ref('<source>_<resource>')}}` pattern in YAML metric definitions.

Every column is typed (strings, numbers, booleans, timestamps), so dates need only `CAST(field AS DATE)`, with no string parsing. Every table also has a `_collected_at` (TIMESTAMP WITH TIME ZONE) column. The tables below list only the fields the current metrics use; see [posture's docs](https://github.com/massyn/posture/blob/main/docs/index.md) for every column of every table.

## Data Source Tables

### **crowdstrike_hosts**
**Purpose**: Host/device inventory from CrowdStrike Falcon  
**Usage**: Used in 18 metrics (vulnerability management, agent coverage and asset discovery)

**Fields**:
- `device_id` (VARCHAR) - Unique device identifier, used for joining with vulnerabilities
- `hostname` (VARCHAR) - Hostname of the device
- `serial_number` (VARCHAR) - Serial number, used to match devices across sources
- `platform_name` (VARCHAR) - 'Mac', 'Windows' or 'Linux'
- `cloud_provider` (VARCHAR) - Set for cloud instances
- `reduced_functionality_mode` (BOOLEAN) - Whether the sensor is running in reduced functionality mode
- `last_seen` (TIMESTAMP WITH TIME ZONE) - Last time the device was seen

**Example Usage**:
```sql
FROM {{ ref('crowdstrike_hosts') }} AS host
WHERE CURRENT_DATE - CAST(host.last_seen AS DATE) < 30
```

### **crowdstrike_vulnerabilities**
**Purpose**: Open vulnerabilities from CrowdStrike Falcon Spotlight  
**Usage**: Used in 15 vulnerability management metrics

**Fields**:
- `id` (VARCHAR) - Unique vulnerability record identifier, used for joining with remediations
- `agent_id` (VARCHAR) - Device ID, used for joining with hosts
- `cve_id` (VARCHAR) - CVE identifier
- `status` (VARCHAR) - Vulnerability status ('open', 'reopen', etc.)
- `severity` (VARCHAR) - Vulnerability severity ('HIGH', 'CRITICAL', etc.)
- `remediation_level` (VARCHAR) - Remediation level ('O' for official patch available)
- `exploit_status` (BIGINT) - Exploit status (>0 indicates exploitable)
- `published_on` (TIMESTAMP WITH TIME ZONE) - CVE publication date
- `created_at` (TIMESTAMP WITH TIME ZONE) - When the vulnerability was first detected on the host

**Example Usage**:
```sql
FROM {{ ref('crowdstrike_vulnerabilities') }} AS cve
WHERE cve.status IN ('open', 'reopen')
  AND cve.severity IN ('HIGH', 'CRITICAL')
  AND coalesce(cve.remediation_level = 'O', false)
  AND coalesce(cve.exploit_status > 0, false)
```

### **crowdstrike_vulnerability_remediations**
**Purpose**: Remediation steps for each CrowdStrike vulnerability (one row per step)  
**Usage**: Used in 7 vulnerability management metrics

**Fields**:
- `id` (VARCHAR) - Vulnerability record identifier, joins to `crowdstrike_vulnerabilities.id`
- `title` (VARCHAR) - Remediation title

### **tenableio_assets**
**Purpose**: Asset inventory from Tenable.io  
**Usage**: Used in 8 vulnerability management metrics

**Fields**:
- `asset_id` (VARCHAR) - Unique asset identifier, used for joining with vulnerabilities
- `hostname` (VARCHAR) - Hostname of the asset
- `last_seen` (TIMESTAMP WITH TIME ZONE) - Last time the asset was seen

**Example Usage**:
```sql
FROM {{ ref('tenableio_assets') }} AS asset
WHERE CURRENT_DATE - CAST(asset.last_seen AS DATE) < 30
```

### **tenableio_vulnerabilities**
**Purpose**: Vulnerability findings from Tenable.io  
**Usage**: Used in 15 vulnerability management metrics

**Fields**:
- `asset_uuid` (VARCHAR) - Asset identifier, joins to `tenableio_assets.asset_id`
- `asset_hostname` (VARCHAR) - Asset hostname
- `state` (VARCHAR) - Finding state ('OPEN', 'REOPENED', etc.)
- `severity` (VARCHAR) - Finding severity ('high', 'critical', etc.)
- `first_found` (TIMESTAMP WITH TIME ZONE) - When the finding was first discovered
- `last_found` (TIMESTAMP WITH TIME ZONE) - When the finding was last seen
- `plugin_id` (BIGINT) - Plugin/check identifier
- `plugin_name` (VARCHAR) - Plugin/check name
- `publication_date` (TIMESTAMP WITH TIME ZONE) - Plugin publication date
- `cve` (VARCHAR) - JSON array of CVE identifiers; read with `from_json(cve, '["VARCHAR"]')`
- `exploit_available` (BOOLEAN) - Whether an exploit is available
- `has_patch` (BOOLEAN) - Whether a patch is available

`exploit_available`, `has_patch` and `publication_date` need posture 1.9.2 or later.

**Example Usage**:
```sql
FROM {{ ref('tenableio_vulnerabilities') }} AS cve
WHERE cve.state IN ('OPEN', 'REOPENED')
  AND cve.severity IN ('high', 'critical')
  AND cve.exploit_available IS TRUE
  AND cve.has_patch IS TRUE
```

### **cve_db_cve_summary**
**Purpose**: One row per CVE from NVD (via [cve-db](https://cve-db.pages.dev)), used to classify vulnerabilities as operating system or application  
**Usage**: Used in 13 vulnerability management metrics (the `_os` and `_apps` variants)

`cve_db` needs no credentials, so `posturecollect` only collects it when named: `posturecollect --include cve_db.cve_summary` (`run.sh` does this).

**Fields**:
- `cve_id` (VARCHAR) - CVE identifier
- `is_os` (BIGINT) - 1 if NVD lists an operating system among the affected products
- `is_app` (BIGINT) - 1 if NVD lists an application among the affected products

A CVE can be both, and a CVE missing from NVD is neither.

### **okta_users**
**Purpose**: User accounts from Okta  
**Usage**: Used in 8 identity management, access control and user security metrics

**Fields**:
- `id` (VARCHAR) - Unique user identifier
- `profile_login` (VARCHAR) - User login/email identifier
- `status` (VARCHAR) - User account status ('ACTIVE', 'SUSPENDED', 'DEPROVISIONED', etc.)
- `status_changed` (TIMESTAMP WITH TIME ZONE) - When the status last changed
- `last_login` (TIMESTAMP WITH TIME ZONE) - Last login
- `password_changed` (TIMESTAMP WITH TIME ZONE) - Password last changed

**Example Usage**:
```sql
FROM {{ ref('okta_users') }}
WHERE status = 'ACTIVE'
  AND CURRENT_DATE - CAST(last_login AS DATE) < 90
```

### **snyk_projects**
**Purpose**: Projects/repositories from Snyk  
**Usage**: Used in 1 software development metric

**Fields**:
- `id` (VARCHAR) - Unique project identifier, used for joining with issues
- `name` (VARCHAR) - Project name

### **snyk_issues**
**Purpose**: Security issues from Snyk  
**Usage**: Used in 1 software development metric

**Fields**:
- `id` (VARCHAR) - Unique issue identifier
- `project_id` (VARCHAR) - Project ID, joins to `snyk_projects.id`
- `status` (VARCHAR) - Issue status ('open', etc.)
- `effective_severity_level` (VARCHAR) - Severity level ('critical', 'high', etc.)

### **knowbe4_training_enrollments**
**Purpose**: Security awareness training enrolments from KnowBe4  
**Usage**: Used in 1 user security metric

**Fields**:
- `user_email` (VARCHAR) - User email, joins to `okta_users.profile_login`
- `completion_date` (TIMESTAMP WITH TIME ZONE) - Training completion date

### **okta_user_factors**
**Purpose**: Authentication factors enrolled by each Okta user  
**Usage**: Used in 2 identity management metrics

**Fields**:
- `user_id` (VARCHAR) - Okta user ID, joins to `okta_users.id`
- `factor_type` (VARCHAR) - Factor type (`signed_nonce` for Okta FastPass, `webauthn`, `push`, `token:software:totp`, etc.)
- `status` (VARCHAR) - Factor status ('ACTIVE', 'PENDING_ACTIVATION', etc.)

### **okta_devices**
**Purpose**: Devices registered with Okta  
**Usage**: Used in 1 data protection metric (Windows devices)

**Fields**:
- `profile_displayname` (VARCHAR) - Device name
- `profile_platform` (VARCHAR) - Platform ('WINDOWS', 'MACOS', 'IOS', 'ANDROID')
- `profile_diskencryptiontype` (VARCHAR) - Disk encryption ('ALL_INTERNAL_VOLUMES', 'FULL', 'USER', 'NONE')
- `status` (VARCHAR) - Device status ('ACTIVE', 'DEACTIVATED')

### **knowbe4_pst_recipients**
**Purpose**: Results of KnowBe4 simulated phishing emails, one row per recipient per test  
**Usage**: Used in 1 user security metric

**Fields**:
- `user_email` (VARCHAR) - Recipient email, joins to `okta_users.profile_login`
- `delivered_at` (TIMESTAMP WITH TIME ZONE) - When the email was delivered
- `clicked_at`, `data_entered_at`, `attachment_opened_at`, `macro_enabled_at`, `qr_code_scanned_at` (TIMESTAMP WITH TIME ZONE) - When the recipient failed the test, if they did

### **kandji_devices**
**Purpose**: Devices managed by Kandji  
**Usage**: Used in 6 metrics (as the device inventory)

**Fields**:
- `device_id` (VARCHAR) - Kandji device ID, joins to `kandji_device_details.device_id`
- `device_name` (VARCHAR) - Device name
- `serial_number` (VARCHAR) - Serial number, used to match devices across sources
- `is_missing`, `is_removed` (BOOLEAN) - Whether the device is missing or removed
- `last_check_in` (TIMESTAMP WITH TIME ZONE) - Last check-in with Kandji

### **kandji_device_details**
**Purpose**: Detailed state of each Kandji device  
**Usage**: Used in 3 metrics

**Fields**:
- `device_id` (VARCHAR) - Kandji device ID
- `device_name`, `serial_number` (VARCHAR) - Device name and serial number
- `platform` (VARCHAR) - 'Mac' or 'Windows'
- `os_version` (VARCHAR) - OS version (e.g. '26.6.2' on a Mac)
- `filevault_enabled` (BOOLEAN) - Whether FileVault disk encryption is on

### **workspaceone_computers**
**Purpose**: Computers managed by Workspace ONE  
**Usage**: Used in 3 metrics (as part of the device inventory)

**Fields**:
- `device_friendly_name` (VARCHAR) - Device name
- `serial_number` (VARCHAR) - Serial number, used to match devices across sources
- `enrollment_status` (VARCHAR) - Enrolment status ('ENROLLED', 'UNENROLLED', etc.)
- `last_seen` (TIMESTAMP WITH TIME ZONE) - Last time the device was seen

### **salesforce_fixed_asset__c**
**Purpose**: The asset register  
**Usage**: Used in 1 asset management metric

**Fields**:
- `serial_number__c` (VARCHAR) - Asset serial number
- `status__c` (VARCHAR) - Asset status ('With Employee', 'On Loan', 'Donated', etc.)

### **salesforce_krow__project_resources__c**
**Purpose**: Staff records  
**Usage**: Used in 1 access control metric

**Fields**:
- `user_email__c` (VARCHAR) - Staff email, joins to `okta_users.profile_login`
- `employment_end_date__c` (TIMESTAMP WITH TIME ZONE) - Employment end date; null while employed

A person can have several records (e.g. when rehired), so treat someone as a leaver only when every record for their email has ended.

### **endoflife_cycles**
**Purpose**: Release cycles and support status of software products, from [endoflife.date](https://endoflife.date)  
**Usage**: Used in 1 vulnerability management metric

**Fields**:
- `product` (VARCHAR) - Product (e.g. 'macos')
- `cycle` (VARCHAR) - Release cycle (e.g. '26' for macOS 26)
- `label` (VARCHAR) - Display name (e.g. 'macOS 26 (Tahoe)')
- `is_eol` (BOOLEAN) - Whether the cycle is end of life
- `eol_from` (TIMESTAMP WITH TIME ZONE) - When it reached end of life

### **macadmins_macos_cves**
**Purpose**: CVEs fixed in each macOS release, from [macadmins.io](https://sofa.macadmins.io)  
**Usage**: Used in 1 vulnerability management metric

**Fields**:
- `product_version` (VARCHAR) - macOS release that fixes the CVE (e.g. '26.7.1')
- `cve_id` (VARCHAR) - CVE identifier
- `exploited` (BOOLEAN) - Whether Apple reports the CVE as actively exploited

`macadmins` needs no credentials, so `posturecollect` only collects it when named with `--include`.

### **cloudflare_zones** and **cloudflare_dns_records**
**Purpose**: DNS zones hosted in Cloudflare, and their records  
**Usage**: Used in 3 network security metrics

**Fields**:
- `cloudflare_zones.id`, `name` (VARCHAR) - Zone ID and domain name
- `cloudflare_dns_records.zone_id` (VARCHAR) - Joins to `cloudflare_zones.id`
- `cloudflare_dns_records.name`, `type`, `content` (VARCHAR) - Fully qualified record name (the zone's own name at the apex), type and value
- `cloudflare_dns_records.proxiable`, `proxied` (BOOLEAN) - Whether the record can be, and is, proxied through Cloudflare

### **dnsimple_domains** and **dnsimple_zone_records**
**Purpose**: Domains registered with DNSimple, and the records of DNSimple-hosted zones  
**Usage**: Used in 3 network security metrics

**Fields**:
- `dnsimple_domains.name` (VARCHAR) - Domain name
- `dnsimple_domains.state` (VARCHAR) - 'registered' or 'hosted' (hosted domains are registered elsewhere)
- `dnsimple_domains.expires_on` (TIMESTAMP WITH TIME ZONE), `auto_renew` (BOOLEAN) - Expiry and auto-renewal
- `dnsimple_zone_records.zone`, `name`, `type`, `content` (VARCHAR) - Zone, record name (empty at the apex), type and value

### **github_repositories** and **github_dependabot_alerts**
**Purpose**: GitHub repositories and their open Dependabot alerts  
**Usage**: Used in 2 software development metrics

**Fields**:
- `github_repositories.org`, `name`, `full_name` (VARCHAR) - Organisation, repository name and `org/name`
- `github_repositories.archived` (BOOLEAN) - Archived repositories are excluded
- `github_dependabot_alerts.org`, `repo` (VARCHAR) - Join to `github_repositories.org` and `name`
- `github_dependabot_alerts.state`, `severity` (VARCHAR) - Only 'open' alerts are collected; severity is 'critical', 'high', 'medium' or 'low'
- `github_dependabot_alerts.cve_id`, `ghsa_id`, `package_name` (VARCHAR) - Advisory and affected package
- `github_dependabot_alerts.created_at` (TIMESTAMP WITH TIME ZONE) - When the alert was raised

## Development Patterns

### **Join Patterns**
- **CrowdStrike**: hosts to vulnerabilities on `host.device_id = cve.agent_id`; vulnerabilities to remediations on `remediation.id = cve.id`
- **Tenable.io**: assets to vulnerabilities on `asset.asset_id = cve.asset_uuid`
- **Okta + KnowBe4**: users to training on `users.profile_login = training.user_email`
- **Snyk**: projects to issues on `projects.id = issues.project_id`
- **Devices across sources** (CrowdStrike, Kandji, Workspace ONE, Salesforce asset register): on `upper(serial_number)`
- **Kandji**: devices to details on `device_id`
- **Okta**: users to factors on `factors.user_id = users.id`
- **Staff to Okta**: on `lower(users.profile_login) = lower(staff.user_email__c)`
- **GitHub**: repositories to Dependabot alerts on `org` and `repo = name`
- **Cloudflare**: zones to records on `records.zone_id = zones.id`

### **Date Handling**
All date fields are typed timestamps. Convert with `CAST(field AS DATE)`. Cast to `VARCHAR` before using one as `detail`.

### **Filtering Active Resources**
Most metrics filter for recently active resources (typically 30 days):
```sql
WHERE CURRENT_DATE - CAST(last_seen AS DATE) < 30
```

### **Vulnerability Classification**
Vulnerabilities are classified by:
- **Severity**: 'HIGH'/'CRITICAL' (CrowdStrike) or 'high'/'critical' (Tenable.io)
- **Status**: 'open'/'reopen' (CrowdStrike) or 'OPEN'/'REOPENED' (Tenable.io)
- **Exploitable**: `exploit_status > 0` (CrowdStrike) or `exploit_available IS TRUE` (Tenable.io)
- **Patchable**: `remediation_level = 'O'` (CrowdStrike) or `has_patch IS TRUE` (Tenable.io)
- **OS or application**: the CVE's `is_os` / `is_app` flag in `cve_db_cve_summary`:

```sql
-- CrowdStrike
cve.cve_id IN (SELECT cve_id FROM {{ ref('cve_db_cve_summary') }} WHERE is_os = 1)

-- Tenable.io (a finding matches if any of its CVEs does)
EXISTS (SELECT 1 FROM {{ ref('cve_db_cve_summary') }} AS summary
        WHERE summary.is_os = 1 AND list_contains(from_json(cve.cve, '["VARCHAR"]'), summary.cve_id))
```

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