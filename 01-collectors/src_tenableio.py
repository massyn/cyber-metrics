from collector import Collector
from dotenv import load_dotenv
from tenable.io import TenableIO
import os

def findings(C):
    tio = TenableIO(
        access_key=os.environ['TIO_ACCESS_KEY'],
        secret_key=os.environ['TIO_SECRET_KEY']
    )
    data = []
    for d in tio.exports.compliance():
        data.append(d)   
    C.store('tenable_findings',data)

def assets(C):
    tio = TenableIO(
        access_key=os.environ['TIO_ACCESS_KEY'],
        secret_key=os.environ['TIO_SECRET_KEY']
    )
    data = []
    for d in tio.exports.assets():
        data.append(d)   
    C.store('tenable_assets',data)

def was(C):
    tio = TenableIO(
        access_key=os.environ['TIO_ACCESS_KEY'],
        secret_key=os.environ['TIO_SECRET_KEY']
    )
    data = []
    for d in tio.was.export():
        data.append(d)
    C.store('tenable_was',data)

def vulnerabilities(C):
    tio = TenableIO(
        access_key=os.environ['TIO_ACCESS_KEY'],
        secret_key=os.environ['TIO_SECRET_KEY']
    )
    data = []
    for d in tio.exports.vulns():
        data.append(d)
    C.store('tenable_vulnerabilities',data)

def meta():
    return {
        'plugin' : 'tenableio',
        'title'  : 'tenableio',
        'link'  : 'https://developer.tenable.com/docs/introduction-to-pytenable',
        'functions' : [ 'findings','assets','was','vulnerabilities'],
        'env' : {
            'TIO_ACCESS_KEY' : None,
            'TIO_SECRET_KEY' : None
        }
    }

def main():
    C = Collector(meta())
    if C.test_environment():
        findings(C)
        assets(C)
        was(C)
        vulnerabilities(C)

if __name__ == '__main__':
    load_dotenv()
    main()