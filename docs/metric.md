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
# {{ data['title'] }}

## Description

{{ data['description'] }}

{% if data['how'] %}
## How we measure it

{{ data['how'] }}
{% endif %}

## Meta Data

| Attribute | Value |
|-----------|-------|
|**Metric id**|`{{ data['metric_id'] }}`|
|**Category**|{{ data['category'] }}|
|**SLO**|{{ "{:.2f}".format(data['slo'][0] * 100) }}% - {{ "{:.2f}".format(data['slo'][1] * 100) }}%|
|**Weight**|{{ data['weight'] }}|
|**Type**|{{ icon(data['type']) }}

## References

|**Framework**|**Ref**|**Domain**|**Control**|
|--|--|--|--|
{% for f in data['framework'] -%}
|{{ f['framework'] }}|{{ f['ref'] }}|{{ f['domain'] }}|{{ f['control'] }}|
{% endfor %}

{% if data['query'] %}
## Code

{% for code in data['query'] %}
```sql
{{ code }}
```
{% endfor %}
{% endif %}