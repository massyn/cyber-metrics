from collector import Collector
import os
from falconpy import Hosts, SpotlightVulnerabilities, ZeroTrustAssessment
import time
from dotenv import load_dotenv

def hosts(C):
    C.lib.log("INFO","src_crowdstrike","- hosts")
    host_detail = []
    host_list = []
    falcon = Hosts(
        client_id=os.environ["FALCON_CLIENT_ID"],
        client_secret=os.environ["FALCON_SECRET"]
    )
    OFFSET = 0
    TOTAL = 1
    LIMIT = 500
    while OFFSET < TOTAL:
        result = falcon.query_devices_by_filter(limit=LIMIT, offset=OFFSET)
        OFFSET = 0
        TOTAL = 0
        returned_device_list = []
        if result["status_code"] == 200:
            OFFSET = result["body"]["meta"]["pagination"]["offset"]
            TOTAL = result["body"]["meta"]["pagination"]["total"]
            returned_device_list = result["body"]["resources"]

            if returned_device_list:
                host_list.append(returned_device_list)
                host_detail += falcon.get_device_details(ids=returned_device_list)["body"]["resources"]
        else:
            C.lib.log("ERROR","src_crowdstrike",f"Something went wrong - {result['status_code']} - {result['body']['errors'][0]['message']}" )
            break
    C.store('crowdstrike_hosts',host_detail)
    return host_list

def vulnerabilities(C):
    C.lib.log("INFO","src_crowdstrike","- vulnerabilities")
    #query_filter = "cve.id:!['']+status:!'closed'+status:!'expired'+last_seen_within:'14'"
    #query_filter = "cve.id:!['']+cve.exprt_rating:['HIGH','CRITICAL']+status:!'closed'+status:!'expired'+last_seen_within:'14'"
    #query_filter = "cve.id:!['']+cve.exprt_rating:['HIGH','CRITICAL']+last_seen_within:'14'"
    query_filter = "cve.id:!['']+last_seen_within:'14'"
    spotlight = SpotlightVulnerabilities(
        client_id=os.environ["FALCON_CLIENT_ID"],
        client_secret=os.environ["FALCON_SECRET"]
    )
    TOTAL = 1
    AFTER = None
    RETURNED = 0
    returned_vulnerabilities = []
    while RETURNED < TOTAL:
        if spotlight.token_expired():
            C.lib.log("WARNING","src_crowdstrike","Token expired...")
            spotlight = SpotlightVulnerabilities(
                client_id=os.environ["FALCON_CLIENT_ID"],
                client_secret=os.environ["FALCON_SECRET"]
            )
            
        C.lib.log("INFO","src_crowdstrike",f"returned = {RETURNED} / {TOTAL}")
        result = spotlight.query_vulnerabilities_combined(
            filter=query_filter,
            after=AFTER,
            sort="updated_timestamp|asc",
            limit=400,
            facet={"cve", "host_info", "remediation"} #, "evaluation_logic"
        )
        # == handle a rate limit
        while result["status_code"] == 429:
            print("Rate limit met, waiting 0.5 seconds to retry.")
            time.sleep(0.5)
            result = spotlight.query_vulnerabilities_combined(
                filter=query_filter,
                after=AFTER,
                #sort="updated_timestamp|asc",
                limit=400,
                facet={"cve", "host_info", "remediation"} #, "evaluation_logic"
            )

        # == successful
        if result["status_code"] == 200:
            AFTER = result["body"]["meta"]["pagination"]["after"]
            TOTAL = result["body"]["meta"]["pagination"]["total"]
            returned_vulnerabilities += result["body"]["resources"]
            RETURNED = len(returned_vulnerabilities)

        else:
            C.lib.log("ERROR","src_crowdstrike",f"Something went wrong - {result['status_code']} - {result['body']['errors'][0]['message']}" )
            break
    C.store('crowdstrike_vulnerabilities',returned_vulnerabilities)

def zero_trust_assessment(C,host_list):
    C.lib.log("INFO","src_crowdstrike","- zero_trust_assessment")
    zta = ZeroTrustAssessment(
        client_id=os.environ["FALCON_CLIENT_ID"],
        client_secret=os.environ["FALCON_SECRET"]
    )
    data = []
    for id_list in host_list:
        data += zta.get_assessment(ids=id_list)['body']['resources']
    C.store('crowdstrike_zero_trust_assessment',data)

def meta():
    return {
        'plugin' : 'crowdstrike',
        'title'  : 'Crowdstrike Falcon',
        'link'  : 'https://www.falconpy.io/',
        'functions' : [ 'hosts', 'vulnerabilities','zero_trust_assessment'],
        'env' : {
            'FALCON_CLIENT_ID' : None,
            'FALCON_SECRET'    : None
        }
    }

def main():
    C = Collector(meta())
    if C.test_environment():
        host_list = hosts(C)
        zero_trust_assessment(C,host_list)
        vulnerabilities(C)

if __name__ == '__main__':
    load_dotenv()
    main()