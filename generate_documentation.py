import sys
import os
from jinja2 import Environment, FileSystemLoader
import importlib
import re
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
    for y in ['type','title','description','slo','references','weight','category']:
        if y not in x:
            print(f" !! ERROR !! - Metric '{x['metric_id']}' missing '{y}'")
            return False
    
    return True

def extract_store(contents):
    pattern = r'store\(["\']([^"\']+)["\']'
    filenames = re.findall(pattern, contents)
    return filenames

def collector_data(src):
    data = []
    if src not in sys.path:
        sys.path.append(src)
    for filename in sorted(os.listdir(src)):
        if filename.startswith('src') and filename.endswith('.py'):
            plugin = os.path.splitext(filename)[0]
            print(f"Plugin : {src}.{plugin}")
            try:
                module = importlib.import_module(f"{src}.{plugin}")
                z = module.meta()
                with open(f"{src}/{filename}",'rt',encoding='utf-8') as q:
                    contents = q.read()
                    z['store'] = extract_store(contents)
                z['filename'] = filename
                data.append(z)
            except ModuleNotFoundError:
                print(f"Plugin '{plugin}' not found.")
            except Exception as e:
                print(f"Plugin '{plugin}' had an error {e}")
    return data

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

col = collector_data('01-collectors')
met = metrics_data('02-metrics')
fw = readCSV('99-templates/framework.csv')
framework = {}
for f in fw:
    if not f['framework'] in framework:
        framework[f['framework']] = {}
    if not f['ref'] in framework[f['framework']]:
        framework[f['framework']][f['ref']] = f

for m in met:
    if not 'framework' in m:
        m['framework'] = []

    for F in ['ISO 27001:2022','CIS 8.1','NIST CSF v2.0']:
        for mf in m.get('references',{}).get(F,[]):
            if str(mf) not in framework[F]:
                print(f"Metric {m['metric_id']} has a missing {F} reference ({mf})")
            else:
                m['framework'].append(framework[F][str(mf)])

render_jinja(col,'collectors.md','00-docs/collectors.md')
render_jinja(met,'metrics.md','00-docs/metrics.md')