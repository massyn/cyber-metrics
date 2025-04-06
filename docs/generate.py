import yaml
import os
from jinja2 import Environment, FileSystemLoader
import csv

def readCSV(file):
    with open(file, 'rt',encoding='utf-8') as q:
        lines = q.read().split("\n")
        return list(csv.DictReader(lines))
    
def render_jinja(data,template,output):
    template_dir = '.'
    env = Environment(loader=FileSystemLoader(template_dir)).get_template(template)
    result = env.render(data = data)
    print(f"Writing {output}")
    with open(output,'wt',encoding='utf-8') as q:
        q.write(result)

def metrics_data(src):
    data = []
    for filename in sorted(os.listdir(src)):
        if filename.startswith('metric_') and filename.endswith('.yml'):
            metric = os.path.splitext(filename)[0]
            print(f"Metric : {metric}")
            with open(f"{src}/{metric}.yml","rt",encoding='utf-8') as y:
                x = yaml.safe_load(y)
                data.append(x)
    return data

def main():
    m = metrics_data('../02-metrics')

    data = {}
    categories = sorted(list({x.get('category') for x in m if 'category' in x}))
    for c in categories:
        data[c] = []

        for n in m:
            if n['category'] == c:
                data[c].append(n)

    render_jinja(data,"index.md","docs/index.md")
    render_jinja(data,"library.md","docs/library.md")
    
    fw = readCSV('../99-templates/framework.csv')

    for metric in m:
        if not 'framework' in metric:
            metric['framework'] = []

        for F in metric.get('references',{}):
            for r in metric['references'][F]:
                # -- find this one in the framework
                for w in fw:
                    if w['framework'].startswith(F) and str(w['ref']) == str(r):
                        metric['framework'].append(w)
        render_jinja(metric,"metric.md",f"docs/{metric['metric_id']}.md")

main()