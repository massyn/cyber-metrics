from collector import Collector
from dotenv import load_dotenv
import os
import whois
import dns.resolver
import requests

def get_server_headers(url):
    try:
        response = requests.get(url, timeout=10)
        headers_dict = dict(response.headers)
        return headers_dict
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {}

def get_domain_info(domain,type):
    try:
        return list(dns.resolver.resolve(domain, type))
    except:
        return []
    
def domains(C):
    data = []
    C.lib.log("INFO","src_domains","- domains")
    for domain in os.environ["DOMAINS"].split(';'):
        w = whois.whois(domain)
        data.append({
            'domain'            : domain,
            'expiration_date'   : w.expiration_date,
            'updated_date'      : w.updated_date,
            'creation_date'     : w.creation_date,
            'name_servers'      : w.name_servers,
            'txt'               : get_domain_info(domain, "TXT"),
            'mx'                : get_domain_info(domain, "MX"),
            'headers'           : 
                {
                    'http'  : get_server_headers(f"http://{domain}"),
                    'https' : get_server_headers(f"https://{domain}"),
                }
        })

    C.store('domains',data)

def meta():
    return {
        'plugin' : 'domains',
        'title'  : 'Domains',
        'link'  : 'https://',
        'functions' : [ 'domains'],
        'env' : {
            'DOMAINS' : None
        }
    }

def main():
    C = Collector(meta())
    if C.test_environment():
        domains(C)

if __name__ == '__main__':
    load_dotenv()
    main()