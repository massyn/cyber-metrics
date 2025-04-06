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