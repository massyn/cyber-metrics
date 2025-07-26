{%- macro icon(text) -%}
    {%- if text == 'control' -%}
        ![control](https://img.shields.io/badge/CONTROL-1E90FF)
    {%- elif text == 'risk' -%}
        ![risk](https://img.shields.io/badge/RISK-DC143C)
    {%- elif text == 'performance' -%}
        ![performance](https://img.shields.io/badge/PERFORMANCE-32CD32)
    {%- else -%}
        {{ text }}
    {%- endif -%}
{%- endmacro -%}

# Cyber Metrics Platform
*Continuous Security Assurance Through Automated Data-Driven Metrics*

The Cyber Metrics Platform transforms raw security tool data into actionable business intelligence for cybersecurity teams. By automatically collecting data from your existing security stack and processing it through standardized metric definitions, the platform provides real-time visibility into security posture, control effectiveness, and operational performance.

## What Makes This Different

**From Data to Decisions**: Rather than manual spreadsheet-based reporting, this platform automatically ingests data from security tools like CrowdStrike, Tenable, Okta, and Snyk, then applies SQL-based metric definitions to generate consistent, comparable measurements.

**Operational Focus**: Metrics are designed around real security operations - vulnerability management prioritization, incident response effectiveness, access control hygiene, and compliance posture - not just checkbox compliance.

**Framework Alignment**: Every metric maps to established frameworks (ISO 27001, CIS Controls, NIST CSF, Essential 8) while maintaining practical utility for day-to-day security operations.

**Multi-Tenant Architecture**: Built for scale with support for multiple storage backends (local files, AWS S3, PostgreSQL, DuckDB) and configurable data retention policies.

## Platform Architecture

### Three-Stage Pipeline

1. **Collect** (`01-collectors/`): Automated data extraction from security tools via APIs
   - CrowdStrike Falcon (endpoints, vulnerabilities)
   - Tenable.io (vulnerability scans, asset inventory)
   - Okta (identity and access management)
   - Snyk (application security, dependencies)
   - KnowBe4 (security awareness training)

2. **Process** (`02-metrics/`): SQL-based metric calculation using YAML definitions
   - DuckDB query engine with Jinja2 templating
   - Standardized output schema (resource, compliance, detail)
   - Configurable SLO thresholds and weighting

3. **Publish** (`03-publish/`): Delivery to dashboards and reporting systems
   - Parquet data format for analytics
   - REST API endpoints for integration
   - Configurable notification thresholds

### Example: Vulnerability Management

The platform includes comprehensive vulnerability management metrics that move beyond simple "count of critical vulnerabilities" to operationally useful measurements:

- **Posture Metrics**: "What percentage of systems have addressed patchable, exploitable OS vulnerabilities?" 
- **Performance Metrics**: "Are we meeting our 7-day SLA for Patch Tuesday Priority vulnerabilities?"
- **Categorization**: Vulnerabilities classified by urgency matrix (Patchable+Exploitable = "Just bloody patch it")

## How to use this guide

### Types of Metrics

| KxI | Description | Example |
|-----|------------|-----------|
| ![control](https://img.shields.io/badge/CONTROL-1E90FF) | A measure that tracks the implementation of actions, processes, or technologies designed to reduce or mitigate risks within the organization. | % of systems with MFA enforced   |
| ![risk](https://img.shields.io/badge/RISK-DC143C) | A measure that provides visibility into existing or potential risks within the organization, helping to assess areas of vulnerability. | % of endpoints with critical vulnerabilities |
| ![performance](https://img.shields.io/badge/PERFORMANCE-32CD32) | A measure that evaluates the efficiency and speed with which a team is executing and delivering on control implementations and operational tasks. | Time to deploy security patches |

### Framework references

The following frameworks are used in the mapping of metrics

* [ISO 27001:2022](https://www.iso.org/standard/27001)
* [CIS 8.1](https://www.cisecurity.org/controls/v8-1)
* [NIST CSF v.2.0](https://csf.tools/reference/nist-cybersecurity-framework/v2-0/)
* [Essential 8](https://www.cyber.gov.au/resources-business-and-government/essential-cyber-security/essential-eight)

## Getting Started

### Quick Start
```bash
# 1. Collect data from your security tools
cd 01-collectors && python wrapper.py

# 2. Generate metrics from collected data  
cd 02-metrics && python metrics.py

# 3. Publish results to your dashboard
cd 03-publish && python publish.py
```

### Configuration
Set environment variables for your security tool APIs and storage preferences. The platform supports multiple simultaneous storage backends - local files, AWS S3, PostgreSQL, and DuckDB.

### Creating Custom Metrics
Define new metrics using YAML files in `02-metrics/`. Each metric specification includes:
- Metadata (title, description, compliance mapping)
- SQL query using `{{ "{{ref('table_name')}}" }}` pattern
- SLO thresholds and performance targets

See `schema.md` for complete data source documentation.

## Contribute

**New Metrics**: Define additional metrics using the YAML specification format  
**New Collectors**: Add support for additional security tools via the collector framework  
**New Publishers**: Integrate with additional dashboard and reporting platforms  

[Submit contributions](https://github.com/massyn/cyber-metrics/issues)

{% for category in data -%}
## {{ category }}

| Metric | Type |
|--------|------|
{% for m in data[category] -%}
|[{{ m['title'] }}]({{ m['metric_id'] }}.md)|{{ icon(m['type']) }}|
{% endfor %}

{% endfor %}