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

# Cyber Metrics
*A curated library of actionable security metrics to power your executive reporting.*

The Cyber Metric Library provides a curated list of measurable security indicators. It’s designed to simplify executive reporting and highlight the maturity of your security controls. This list focuses on technical metrics that are easy to track using commonly available tools.

## How to use this guide

### Types of Metrics

* ![control](https://img.shields.io/badge/CONTROL-1E90FF) A measure that tracks the implementation of actions, processes, or technologies designed to reduce or mitigate risks within the organization.
* ![risk](https://img.shields.io/badge/RISK-DC143C) A measure that provides visibility into existing or potential risks within the organization, helping to assess areas of vulnerability.
* ![performance](https://img.shields.io/badge/PERFORMANCE-32CD32) A measure that evaluates the efficiency and speed with which a team is executing and delivering on control implementations and operational tasks.

#### Examples

- ![control](https://img.shields.io/badge/CONTROL-1E90FF) % of systems with MFA enforced  
- ![risk](https://img.shields.io/badge/RISK-DC143C) % of endpoints with critical vulnerabilities  
- ![performance](https://img.shields.io/badge/PERFORMANCE-32CD32) Time to deploy security patches  


### Framework references

The following frameworks are used in the mapping of metrics

* [ISO 27001:2022](https://www.iso.org/standard/27001)
* [CIS 8.1](https://www.cisecurity.org/controls/v8-1)
* [NIST CSF v.2.0](https://csf.tools/reference/nist-cybersecurity-framework/v2-0/)
* [Essential 8](https://www.cyber.gov.au/resources-business-and-government/essential-cyber-security/essential-eight)

## Contribute

Looking to contribute new metrics? [Submit a new metric request](https://github.com/massyn/cyber-metrics/issues)

{% for category in data -%}
## {{ category }}

| Metric | Type |
|--------|------|
{% for m in data[category] -%}
|[{{ m['title'] }}]({{ m['metric_id'] }}.md)|{{ icon(m['type']) }}|
{% endfor %}

{% endfor %}