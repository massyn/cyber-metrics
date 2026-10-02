import sys
import os
from jinja2 import Environment, FileSystemLoader
import yaml
import csv

def readCSV(file):
    with open(file, 'rt',encoding='utf-8') as q:
        lines = q.read().split("\n")
        return list(csv.DictReader(lines))
    
def validate_metric(x):
    if 'metric_id' not in x:
        print(f" !! ERROR !! - Metric missing 'metric_id'")
        return False
    for y in ['type','title','description','slo','references','weight','category','enabled','type','query']:
        if y not in x:
            print(f" !! ERROR !! - Metric '{x['metric_id']}' missing '{y}'")
            return False
    
    if x.get('category') not in ['Access Control','Vulnerability Management','User Security','Software Development','Identity Management','Network Security','Disaster Recovery','Data Protection','Malware Protection','Asset Management']:
        print(f" !! ERROR !! - Metric '{x['metric_id']}' has a mismatched category '{x['category']}'")
        return False
    
    return True

def metrics_data(src):
    data = []
    if src not in sys.path:
        sys.path.append(src)
    for filename in sorted(os.listdir(src)):
        if filename.startswith('metric_') and filename.endswith('.yml'):
            metric = os.path.splitext(filename)[0]
            print(f"Metric : {metric}")
            with open(f"{src}/{metric}.yml","rt",encoding='utf-8') as y:
                x = yaml.safe_load(y)
                if validate_metric(x):
                    data.append(x)
    return data

def render_jinja(data,template,output):
    template_dir = '99-templates'
    env = Environment(loader=FileSystemLoader(template_dir)).get_template(template)
    result = env.render(data = data)
    print(f"Writing {output}")
    with open(output,'wt',encoding='utf-8') as q:
        q.write(result)

met = metrics_data('02-metrics')
fw = readCSV('99-templates/framework.csv')

for m in met:
    if not 'framework' in m:
        m['framework'] = []

    for F in m.get('references',{}):
        for r in m['references'][F]:
            # -- find this one in the framework
            found = False
            for w in fw:
                if w['framework'].startswith(F) and str(w['ref']) == str(r):
                    found = True
                    m['framework'].append(w)
            if not found:
                print(f"Could not find {F} - {r} in {m['metric_id']} ")

render_jinja(met,'metrics.md','00-docs/metrics.md')