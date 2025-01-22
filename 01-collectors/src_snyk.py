from collector import Collector
from dotenv import load_dotenv
import requests
import os

def meta():
    return {
        'plugin' : 'snyk',
        'title'  : 'Snyk',
        'link'  : 'https://docs.snyk.io/snyk-api',
        'functions' : [ 'organizations','members','projects','issues'],
        'env' : {
            'SNYK_TOKEN' : None,
            'SNYK_ENDPOINT' : 'https://api.snyk.io'
        }
    }

def call(C,url):
    C.lib.log("INFO","src_snyk",f"Calling ({url})")
    data = []
    headers = {
        'Authorization' : os.environ['SNYK_TOKEN'],
        'Content-Type' : 'application/json; charset=utf-8',
    }
    while True:
        req = requests.get(f"{os.environ['SNYK_ENDPOINT']}{url}",headers=headers,timeout=30)
        if req.status_code != 200:
            print("==============================")
            print(f"something went wrong - {req.status_code}")
            print(f"url = {os.environ['SNYK_ENDPOINT']}{url}")
            print(req.content)
            print("==============================")
            break
        else:
            if not 'data' in req.json():
                data += req.json()
                break
            else:
                data += req.json()['data']
                
                if 'next' in req.json()['links']:
                    url = req.json()['links']['next']
                else:
                    break
    return data

def organizations(C):
    data = call(C,'/rest/orgs?version=2024-08-25&limit=100')
    C.store('snyk_organizations',data)
    return data

def members(C,org):
    data = []
    for o in org:
        data += call(C,f"/v1/org/{o['id']}/members?includeGroupAdmins=true")
    C.store('snyk_members',data)
    return data

def issues(C,org):
    data = []
    for o in org:
        data += call(C,f"/rest/orgs/{o['id']}/issues?version=2024-08-25&limit=100")
    C.store('snyk_issues',data)
    return data
    
def projects(C,org):
    data = []
    for o in org:
        data += call(C,f"/rest/orgs/{o['id']}/projects?version=2024-08-25&limit=100")
    C.store('snyk_projects',data)
    return data

def main():
    C = Collector(meta())
    if C.test_environment():
        org = organizations(C)
        members(C,org)
        projects(C,org)
        issues(C,org)

if __name__ == '__main__':
    load_dotenv()
    main()