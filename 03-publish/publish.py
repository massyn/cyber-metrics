import argparse
import pandas as pd
import os
import sys
from dotenv import load_dotenv
sys.path.append('../')
from library import Library
import requests

class Publish:
    def __init__(self,**KW):
        self.lib = Library()
        
    def upload_to_dashboard(self,df):
        ENDPOINT = os.getenv("CYBER_DASHBOARD_ENDPOINT")
        TOKEN = os.getenv("CYBER_DASHBOARD_TOKEN")

        if not all([ENDPOINT, TOKEN]):
            self.lib.log("WARNING","upload_to_dashboard","One or more dashboard environment variables are not set.")
            return

        csv_data = df.to_csv(index=False)

        self.lib.log("INFO","upload_to_dashboard",f"Uploading {len(df)} records to the dashboard...")
        try:
            response = requests.post(ENDPOINT, headers={
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "text/csv"
            }, data=csv_data)

            if response.status_code == 200:
                self.lib.log("SUCCESS","upload_to_dashboard","Data successfully uploaded to the dashboard.")
            else:
                self.lib.log("ERROR","upload_to_dashboard",f"Error uploading data to the dashboard: {response.status_code}",True)
                self.lib.log("ERROR","upload_to_dashboard",response.text)
        except Exception as e:
            self.lib.log("ERROR","upload_to_dashboard",f"Error uploading data to the dashboard: {e}",True)

def main(**KW):
    load_dotenv()
    P = Publish()

    if not os.path.exists(KW['parquet']):
        P.lib.log("ERROR","main",f"File {KW['parquet']} does not exist")
        exit(1)
    P.lib.log("INFO","main",f"Reading parquet file {KW['parquet']}")
    df = pd.read_parquet(KW['parquet'])
    
    # == Upload the resulting data to their respective destinations
    P.upload_to_dashboard(df)

    P.lib.log("INFO","main","All done")

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Cyber Dashboard - Publish metrics')
    parser.add_argument('-parquet',help='The path where the metrics saves the resulting parquet file',default='../data/detail.parquet')

    args = parser.parse_args()

    main(
        parquet         = args.parquet
    )