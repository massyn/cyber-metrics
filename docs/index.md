{%- macro icon(text) -%}
    {%- if text == 'control' -%}
        ![control](https://img.shields.io/badge/CONTROL-0000F0)
    {%- elif text == 'risk' -%}
        ![risk](https://img.shields.io/badge/RISK-c00000)
    {%- elif text == 'performance' -%}
        ![performance](https://img.shields.io/badge/PERFORMANCE-0F00)
    {%- else -%}
        {{ text }}
    {%- endif -%}
{%- endmacro -%}
# Cyber Metrics

The Cyber Metric Library is a list of security metrics that can be used as a baseline for any executive reporting platform.  The list is not exhaustive, and is focussed primarily on technical controls that can be measured easily with available tooling.

## How to use this guide

### Types of Metrics

* ![control](https://img.shields.io/badge/CONTROL-0000F0) A measure that tracks the implementation of actions, processes, or technologies designed to reduce or mitigate risks within the organization.
* ![risk](https://img.shields.io/badge/RISK-c00000) A measure that provides visibility into existing or potential risks within the organization, helping to assess areas of vulnerability.
* ![performance](https://img.shields.io/badge/PERFORMANCE-0F00) A measure that evaluates the efficiency and speed with which a team is executing and delivering on control implementations and operational tasks.

### Framework references

The following frameworks are used in the mapping of metrics

* [ISO 27001:2022](https://www.iso.org/standard/27001)
* [CIS 8.1](https://www.cisecurity.org/controls/v8-1)
* [NIST CSF v.2.0](https://csf.tools/reference/nist-cybersecurity-framework/v2-0/)
* [Essential 8](https://www.cyber.gov.au/resources-business-and-government/essential-cyber-security/essential-eight)

{% for category in data -%}
## {{ category }}

| Metric | Type |
|--------|------|
{% for m in data[category] -%}
|[{{ m['title'] }}]({{ m['metric_id'] }}.md)|{{ icon(m['type']) }}|
{% endfor %}

{% endfor %}