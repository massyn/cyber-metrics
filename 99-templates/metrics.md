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
{%- macro anchor(text) -%}
    [{{text}}](#{{ text | lower | replace(' ', '-') }})
{%- endmacro -%}

{% set unique_categories = data | map(attribute='category') | map('default', '') | unique | list %}

# Metrics

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

|**Category**|**Title**|**Type**|**Query**|
|--|--|--|--|
{% for a in unique_categories %}|**{{ a }}**|||||
{% for x in data if x['category'] == a -%}
||{{ anchor(x['title']) }}|{{ icon(x['type']) }}|{{ "![yes](https://img.shields.io/badge/YES-00F0)" if x.get('query') is not none else "![No](https://img.shields.io/badge/NO-00F)" }}|
{% endfor -%}
{% endfor %}

## List of metrics

{%- for x in data %}
### {{ x['title'] }}

#### Description

{{ x['description'] }}

#### Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`{{ x['metric_id'] }}`|
|**Category**|{{ x['category'] }}|
|**SLO**|{{ "{:.2f}".format(x['slo'][0] * 100) }}% - {{ "{:.2f}".format(x['slo'][1] * 100) }}%|
|**Weight**|{{ x['weight'] }}|
|**Type**|{{ icon(x['type']) }}

#### References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
{% for f in x['framework'] -%}
|{{ f['framework'] }}|{{ f['ref'] }}|{{ f['domain'] }}|{{ f['control'] }}|
{% endfor %}


{% endfor %}