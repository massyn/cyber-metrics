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

{% for category in data -%}
## {{ category }}

| Metric | Type |
|--------|------|
{% for m in data[category] -%}
|[{{ m['title'] }}]({{ m['metric_id'] }}.md)|{{ icon(m['type']) }}|
{% endfor %}

{% endfor %}