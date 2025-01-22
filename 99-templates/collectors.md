# Collectors

|**Plugin**|**Functions**|**Environment**|**Default value**|
|--|--|--|--|
{% for x in data %}|**[{{ x['title'] }}]({{ x['link'] }})**|{% for y in x['functions'] %}`{{ y }}`<br>{% endfor %}|||
{% for z in x['env'] %}|||`{{ z }}`|`{{ x['env'][z] }}`|
{% endfor %}{% endfor %}