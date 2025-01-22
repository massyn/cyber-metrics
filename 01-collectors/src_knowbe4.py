import requests
from collector import Collector
from dotenv import load_dotenv
import os
import time

def enrollments(C):
    C.lib.log("INFO", "src_knowbe4","- enrollments")
    headers = {
        "Authorization": f"Bearer {os.environ['KNOWBE4_TOKEN']}",
        "Accept": "application/json",
    }
    result = []
    page = 1
    max_retries = 5
    backoff_factor = 1  # Base seconds for backoff

    while True:
        retry_count = 0
        while retry_count < max_retries:
            try:
                C.lib.log("INFO", "src_knowbe4", f"Fetching page {page}")
                req = requests.get(
                    f"{os.environ['KNOWBE4_ENDPOINT']}?page={page}",
                    headers=headers,
                    timeout=30
                )
                req.raise_for_status()
                
                # Check if we hit rate limit (429)
                if req.status_code == 429:
                    retry_after = int(req.headers.get("Retry-After", backoff_factor))
                    C.lib.log("WARNING","src_knowbe4", f"Rate limit hit. Retrying after {retry_after} seconds...")
                    time.sleep(retry_after)
                    retry_count += 1
                    backoff_factor *= 2  # Exponential backoff
                    continue

                # Break out of retry loop on success
                break
            except requests.exceptions.HTTPError as err:
                if req.status_code != 429:
                    C.lib.log("ERROR", "src_knowbe4", f"HTTP error: {err}")
                    break
            except requests.exceptions.RequestException as e:
                C.lib.log("ERROR", "src_knowbe4",f"Request failed: {e}")
                break
            time.sleep(backoff_factor)

        if req.status_code == 429 and retry_count >= max_retries:
            C.lib.log("ERROR", "src_knowbe4", "Max retries reached. Exiting.")
            break

        if req.status_code != 200:
            break
        
        result += req.json()
        page += 1

        if not req.json():
            break

    C.store('knowbe4_enrollments', result)

def meta():
    return {
        'plugin' : 'knowbe4',
        'title'  : 'Knowbe4',
        'link'  : 'https://www.knowbe4.com/',
        'functions' : [ 'enrollments'],
        'env' : {
            'KNOWBE4_TOKEN'     : None,
            'KNOWBE4_ENDPOINT'  : 'https://us.api.knowbe4.com/v1/training/enrollments'
        }
    }

def main():
    C = Collector(meta())
    if C.test_environment():
        enrollments(C)

if __name__ == '__main__':
    load_dotenv()
    main()
