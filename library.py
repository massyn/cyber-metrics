'''A common library used across the Automated Security Platform'''
import os
import datetime
import requests
import json
import boto3
from botocore.exceptions import ClientError
import uuid

class Library:
    def __init__(self):
        self.config = {
            "tenancy"               : os.environ.get('TENANCY','default'),
            "STORE_FILE"            : os.environ.get('STORE_FILE','../data/source/%TAG/%TENANCY.json'),
            "STORE_AWS_S3_BUCKET"   : os.environ.get('STORE_AWS_S3_BUCKET',''),
            "STORE_AWS_S3_WEB"      : os.environ.get('STORE_AWS_S3_WEB',''),
            "STORE_AWS_S3_BACKUP"   : os.environ.get('STORE_AWS_S3_BACKUP','backup/%TAG/%TENANCY.json'),
            "STORE_AWS_S3_KEY"      : os.environ.get('STORE_AWS_S3_KEY',''),
            "STORE_DUCKDB"          : os.environ.get('STORE_DUCKDB',''),
            "STORE_AWS_S3_HISTORY"  : os.environ.get('STORE_AWS_S3_HISTORY','history')
        }
        
        self.datetime = datetime.datetime.now(datetime.timezone.utc)
        self.datestamp = self.datetime.strftime('%Y-%m-%d')

    def log(self,sev,mod,txt,alert = False):
        ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%H:%S')
        print(f"{ts} [{sev:^9}] {mod:^16} : {txt}")

        if alert and os.environ.get('SLACK_WEBHOOK','') != '':
            severity_icons = {
                'ERROR': ':x:',      # Red Cross
                'INFO': ':information_source:',  # Information Icon
                'SUCCESS': ':white_check_mark:', # Checkmark
                'WARNING': ':warning:'          # Warning Icon
            }
            icon = severity_icons.get(sev, '')
            message = f"{icon} {txt}" if icon else txt
            try:
                x = requests.post(os.environ['SLACK_WEBHOOK'],data=json.dumps({ 'type': 'mrkdwn', 'text' : message }).encode('utf-8'),headers = {   
                    'Content-Type': 'application/json'})
                self.log("SUCCESS","slack",f"Slack Response Code: {x.status_code}")
            except Exception as e:
                self.log("WARNING","slack",f"Error sending Slack alert: {e}")
    
    def variables(self,tag,input):
        if tag == None:
            tag = ''
        if input == None:
            input = ''
        return input.replace(
            '%UUID',str(uuid.uuid4())).replace(
            '%TAG',tag).replace(
            '%TENANCY',self.config['tenancy']).replace(
            '%hh',self.datetime.strftime('%H')).replace(
            '%mm',self.datetime.strftime('%M')).replace(
            '%ss',self.datetime.strftime('%S')).replace(
            '%YYYY',self.datetime.strftime('%Y')).replace(
            '%MM',self.datetime.strftime('%m')).replace(
            '%DD',self.datetime.strftime('%d')
        )
    
    def backup_to_s3(self,file_name,bucket,key):
        if bucket != '' and bucket != None and key != '' and key != None and file_name != None and file_name != '':
            self.log("INFO","backup_to_s3",f"bucket    = {bucket}")
            self.log("INFO","backup_to_s3",f"key       = {key}")
            self.log("INFO","backup_to_s3",f"file_name = {file_name}")
            s3_client = boto3.client('s3')
            if os.path.exists(file_name):    
                try:
                    s3_client.upload_file(file_name, bucket, key, ExtraArgs={'ACL': 'bucket-owner-full-control'})
                    self.log("SUCCESS","backup_to_s3",f"Upload complete.")
                except ClientError as e:
                    self.log("ERROR","backup_to_s3",e)
            else:
                self.log("WARNING","backup_to_s3",f"The file {file_name} does not exist, so we will try to grab it from S3")
                try:
                    s3_client.download_file(bucket, key, file_name)
                    self.log("SUCCESS","backup_to_s3",f"Downloaded from s3://{bucket}/{key} --> {file_name}")
                except ClientError as e:
                    self.log("ERROR","backup_to_s3",e)

    def upload_to_s3(self,file_name,bucket,key):
        self.log("INFO","upload_to_s3",f"Bucket = {bucket} , key = {key}, file_name = {file_name} ...")
        if not os.path.exists(file_name):
            self.log("WARNING","upload_to_s3",f"Not uploading to S3 because {file_name} does not exist")
        else:
            if bucket != None and bucket != '' and key != None and os.path.exists(file_name):
                self.log("INFO","upload_to_s3",f"Uploading {file_name} to s3://{bucket}/{key}")
                s3_client = boto3.client('s3')
                try:
                    s3_client.upload_file(file_name, bucket, key, ExtraArgs={'ACL': 'bucket-owner-full-control'})
                    self.log("SUCCESS","upload_to_s3",f"Upload complete.")
                except ClientError as e:
                    self.log("ERROR","upload_to_s3",e)
                    return False
                return True
            else:
                self.log("WARNING","upload_to_s3","Not uploading to S3 because none of the variables are defined.")

    def download_from_s3(self,bucket,key,target = 'blob',parameter = None):
        if bucket != '' and bucket != None and key != '' and key != None:
            self.log("INFO","download_from_s3",f"Bucket    = {bucket}")
            self.log("INFO","download_from_s3",f"Key       = {key}")
            self.log("INFO","download_from_s3",f"Target    = {target}")
            self.log("INFO","download_from_s3",f"Parameter = {parameter}")

            s3_client = boto3.client('s3')
            if target == 'file':
                try:
                    s3_client.download_file(bucket, key, parameter)
                    self.log("SUCCESS","download_from_s3",f"Downloaded from s3://{bucket}/{key} --> {parameter}")
                    return True
                except ClientError as e:
                    self.log("ERROR","download_from_s3",e)
                    return False
            else:
                print("TODO")
                exit(1)

        else:
            self.log("WARNING","download_from_s3","Not downloading since bucket or key is not defined")
