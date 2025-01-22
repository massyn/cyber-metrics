import os
import uuid
import json
import datetime
import duckdb
import boto3
import botocore
import psycopg2
from psycopg2 import Error
import sys
sys.path.append('../')
from library import Library

class Collector:
    def __init__(self,meta = { 'title' : 'Collector'}):
        
        self.meta = meta
        self.lib = Library()
        self.datetime = datetime.datetime.now(datetime.timezone.utc)
        self.upload_timestamp = self.datetime.strftime('%Y-%m-%d %H:%M:%S')
        self.upload_id = str(uuid.uuid4())
        
    def test_environment(self):
        ok = True
        for v in self.meta['env']:
            # we only care if the environment variable is not set.
            if not os.environ.get(v):
                if self.meta['env'][v] is not None:
                    os.environ[v] = self.meta['env'][v]
                else:
                    self.lib.log("WARNING","test_environment",f"Environment variable {v} not found")
                    ok = False
        return ok
        
    def check_env(self,v,default = None):
        if not v in os.environ:
            if default != None:
                return default
        else:
            return os.environ[v]

    def add_meta(self,data):
        new = []
        for i in data:
            i['_tenancy'] = self.lib.config['tenancy']
            i['_upload_timestamp'] = self.upload_timestamp
            i['_upload_id'] = self.upload_id
            new.append(i)
        return new
    
    def store(self,tag,data1):
        if len(data1) > 0:
            self.lib.log("INFO","store",f"Storing {tag} of {len(data1)} records")

            data = self.add_meta(data1)

            self.store_file(tag,data)
            self.lib.backup_to_s3(
                self.lib.variables(tag,self.lib.config['STORE_FILE']),
                self.lib.config['STORE_AWS_S3_BUCKET'],
                self.lib.variables(tag,self.lib.config['STORE_AWS_S3_BACKUP'])
            )
            self.upload_to_s3(data,tag,self.lib.config['STORE_AWS_S3_KEY'])
            self.store_postgres(tag,data)
            self.store_duckdb(tag,data)
        else:
            self.lib.log("WARNING","store",f"No records to be written to {tag} - empty data set")
    
    def store_file(self,tag,data):
        target = self.lib.variables(tag,self.lib.config['STORE_FILE'])
        try:
            os.makedirs(os.path.dirname(target),exist_ok = True)        
            with open(target,"wt",encoding='UTF-8') as q:
                q.write(json.dumps(data,default=str))
            self.lib.log("SUCCESS","store_file",f"Saving {len(data)} records for {tag} --> {target}")
        except:
            self.lib.log("ERROR",f"Cannot write the file - {target}")

    def upload_to_s3(self,data,tag,target):
        key = self.lib.variables(tag,target)
        if key != '' and self.lib.config['STORE_AWS_S3_BUCKET'] != '':
            self.lib.log("INFO","upload_to_s3",f"Saving {len(data)} records for {tag} --> s3://{self.lib.config['STORE_AWS_S3_BUCKET']}/{key}")
            try:
                boto3.resource('s3').Bucket(self.lib.config['STORE_AWS_S3_BUCKET']).put_object(
                    ACL         = 'bucket-owner-full-control',
                    ContentType = 'application/json',
                    Key         = key,
                    Body        = json.dumps(data,default=str)
                )
                self.lib.log("SUCCESS","upload_to_s3",f"s3.put_object - s3://{self.check_env('STORE_AWS_S3_BUCKET')}/{target}")
            except botocore.exceptions.ClientError as error:
                self.lib.log("ERROR","upload_to_s3",f"s3.put_object - {error.response['Error']['Code']}")
            except:
                self.lib.log("ERROR","upload_to_s3",f"s3.put_object")
        else:
            self.lib.log("WARNING","upload_to_s3",f"- Not uploading to S3...")

    def store_postgres(self,tag,data):
        host        = self.check_env('STORE_POSTGRES_HOST')
        user        = self.check_env('STORE_POSTGRES_USER')
        password    = self.check_env('STORE_POSTGRES_PASSWORD')
        dbname      = self.check_env('STORE_POSTGRES_DBNAME')
        port        = self.check_env('STORE_POSTGRES_PORT')
        schema      = self.check_env('STORE_POSTGRES_SCHEMA')

        if host:
            try:
            # Connect to your PostgreSQL database
                con = psycopg2.connect(
                    user        = user,
                    password    = password,
                    host        = host,
                    port        = port,
                    database    = dbname,
                )
            except (Exception, Error) as error:
                self.con = False
                self.lib.log("ERROR","store_postgres",f"Postgres - Unable to connect : {host}")
                return

            if con:
                self.lib.log("SUCCESS","store_postgres",f"Postgres : Connected : {host}")

                try:
                    cursor = con.cursor()
                    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
                    con.commit()
                except (Exception, Error) as error:
                    self.lib.log("ERROR","store_postgres",f"Postgres - Unable to create schema : {error}")

                try:
                    cursor.execute(f"CREATE TABLE IF NOT EXISTS {schema}.{tag} (upload_timestamp timestamp, tenancy VARCHAR, json_data json)")
                except (Exception, Error) as error:
                    self.lib.log("ERROR","store_postgres",f"Postgres - Unable to create table : {error}")
                con.commit()

                # -- insert data
                for d in data:
                    try:
                        cursor.execute(f"INSERT INTO {schema}.{tag} (upload_timestamp,tenancy,json_data) VALUES(%s,%s,%s)",(self.upload_timestamp,self.lib.config['tenancy'],json.dumps(d)))
                    except (Exception, Error) as error:
                        self.lib.log("ERROR","store_postgres",f"Postgres - Unable to insert record : {error}")
                con.commit()
                cursor.close()
                self.lib.log("SUCCESS","store_postgres",f"Postgres - {tag} - Inserted {len(data)} records.")

    def store_duckdb(self,tag,data):
        target = self.lib.variables(tag,self.lib.config['STORE_DUCKDB'])
        if target != '':
            try:
                db = duckdb.connect(database = target, read_only = False)
                self.lib.log("SUCCESS","store_duckdb",f"DuckDB : Connected : {target}")
            except:
                db = False
                self.lib.log("ERROR","store_duckdb",f"DuckDB - Unable to connect : {target}")

            if db:
                # -- create table
                cursor = db.cursor()
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {tag} (upload_timestamp timestamp, tenancy VARCHAR, json_data TEXT)")
                db.commit()

                # -- insert data
                for d in data:
                    cursor.execute(f"INSERT INTO {tag} (upload_timestamp,tenancy,json_data) VALUES(?,?,?)",(self.upload_timestamp,self.lib.config['tenancy'],json.dumps(d)))
                db.commit()
                cursor.close()
                self.lib.log("SUCCESS","store_duckdb",f"DuckDB - {tag} - Inserted {len(data)} records.")
