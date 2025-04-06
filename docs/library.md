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

# Library List

| Category | Metric | Type |
|----------|--------|------|
{% for category, metrics in data.items() -%}
  {% for m in metrics -%}
| {{ category if loop.first else '' }} | [{{ m['title'] }}]({{ m['metric_id'] }}.md) | {{ icon(m['type']) }} |
  {% endfor -%}
{% endfor %}
