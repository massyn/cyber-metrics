import duckdb
import yaml
from jinja2 import Environment, FileSystemLoader
import os
import datetime
import pandas as pd
import argparse
import tabulate
import glob
import sys
from dotenv import load_dotenv
sys.path.append('../')
from library import Library

class Metric:
    def __init__(self,**KW):
        self.lib = Library()
        
        if KW.get('data_path'):
            self.data_path = KW['data_path']
            self.lib.log("INFO","init",f"Data Path = {self.data_path}")
        else:
            self.lib.log("ERROR","init","No data path specified")
            exit(1)

        self.privacy = KW.get('privacy',True)
        if self.privacy == True:
            self.lib.log("WARNING","init","Privacy mode is enabled.  Resource and Detail will be redacted.  If you need to see that info, run with -privacy_off")
        
        self.datestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
        self.lib.log("INFO","init",f"Datestamp = {self.datestamp}")
        self.history = []
        self.privacy = True
        self.data_tables = {}

    def resolve_ref(self, table_name):
        self.data_tables[table_name] = f"{self.data_path}/{table_name}/*.json"
        col = ''
        if table_name == 'crowdstrike_hosts':
            col = ",columns={'last_seen': 'VARCHAR','device_id' : 'VARCHAR','hostname' : 'VARCHAR'}"

        return f"read_json('{self.data_tables[table_name]}'{col})"
        
    def metric_run(self,yaml_config,query):
        if yaml_config.get('enabled',True) == False or query == None:
            self.lib.log("INFO","metric_run",f"Metric {yaml_config['metric_id']} is disabled")
            return pd.DataFrame()
        self.data_tables = {}
        env = Environment(loader=FileSystemLoader('.'))
        env.globals['ref'] = self.resolve_ref
        template = env.from_string(query).render()

        # == check if the tables defined in the SQL query actually exist
        success = True
        for table in self.data_tables:
            if len(glob.glob(self.data_tables[table])) > 0:
                self.lib.log("INFO","metric_run",f"Table {table} exists")
            else:
                self.lib.log("ERROR","metric_run",f"Table {table} does not exist ({self.data_tables[table]})")
                success = False
        if not success:
            return pd.DataFrame()

        # == execute the query
        try:
            # Execute query
            df = duckdb.query(template).df()
            self.lib.log("SUCCESS","metric_run",f"Retrieved {len(df)} records")
            if args.dryrun:
                print(df)
        except duckdb.Error as e:
            self.lib.log("ERROR","metric_run",f"Failed to execute query: {e}")
            print(template)
            return pd.DataFrame()
        
        # == if privacy is enabled, we hide resource and detail
        if self.privacy:
            df['resource'] = 'redacted - privacy enabled'
            df['detail'] = 'redacted - privacy enabled'

        # == check if the mandatory columns are there
        success = True
        for col in [ 'resource','resource_type','compliance','detail']:
            if not col in df.columns:
                self.lib.log("ERROR","metric_run",f" - Column {col} does not exists.  Check the SQL in your metric defintion")
                success = False
        if not success:
            return pd.DataFrame()

        # == add the meta data
        success = True

        if 'metric_id' in yaml_config:
            df['metric_id'] = yaml_config['metric_id']
        else:
            self.lib.log("ERROR","metric_run","metric_id is missing in meta data")
            success = False
        
        if 'title' in yaml_config:
            df['title'] = yaml_config['title']
        else:
            self.lib.log("ERROR","metric_run","title is missing in meta data")
            success = False
        
        if 'category' in yaml_config:
            df['category'] = yaml_config['category']
        else:
            self.lib.log("ERROR","metric_run","category is missing in meta data")
            success = False

        if 'weight' in yaml_config:
            if float(yaml_config['weight']) >= 0 and float(yaml_config['weight']) <= 1:
                df['weight'] = yaml_config['weight']
            else:
                self.lib.log("ERROR","metric_run","weight is not a percentage between 0 and 1")
                success = False
        else:
            self.lib.log("ERROR","metric_run","weight is missing in meta data")
            success = False

        if 'slo' in yaml_config:
            if isinstance(yaml_config['slo'],list) and len(yaml_config['slo']) == 2:
                if float(yaml_config['slo'][0]) >= 0 and float(yaml_config['slo'][0]) <= 1:
                    df['slo_min'] = yaml_config['slo'][0]
                else:
                    self.lib.log("ERROR","metric_run","slo[0] needs to be a percentage between 0 and 1")
                    success = False
                if float(yaml_config['slo'][1]) >= 0 and float(yaml_config['slo'][1]) <= 1:
                    df['slo'] = yaml_config['slo'][1]
                else:
                    self.lib.log("ERROR","metric_run","slo[0] needs to be a percentage between 0 and 1")
                    success = False
            else:
                self.lib.log("ERROR","metric_run","slo is not a list with two values")
                success = False
        else:
            self.lib.log("ERROR","metric_run","slo is missing in meta data")
            success = False

        if not success:
            return pd.DataFrame()
        df['datestamp'] = self.datestamp
        df['datestamp'] = pd.to_datetime(df['datestamp']).dt.date

        # == Merge the resource dimensions - TODO
        # == if we got the dimension from the query, we don't need to do anything
        # == it is when we did not get it from the query, we need to apply it here
        for dim in ['business_unit','team','location']:
            if dim not in df.columns:
                df[dim] = 'undefined'   ## TODO
        
        return df

def main(**KW):
    load_dotenv()
    M = Metric(data_path = KW['data_path'])

    # should we send an alert?
    alert = not (KW.get('dryrun') or KW.get('metric'))

    df_detail = pd.DataFrame()

    for filename in os.listdir(KW['metric_path']):
        if filename.startswith('metric_') and filename.endswith('.yml'):
            metric_file = os.path.splitext(filename)[0]
            with open(f"{KW['metric_path']}/{metric_file}.yml",'rt') as y:
                metric = yaml.safe_load(y)
            
            if KW['metric'] == None or KW['metric'] == metric_file or KW['metric'] == metric['metric_id']:
                M.lib.log("INFO","main","-----------------------------------------------------------------------")
                M.lib.log("INFO","main",f"Metric : {metric_file}")
                df_metric = pd.DataFrame()
                if 'query' in metric and metric['query'] != None:
                    for i,query in enumerate(metric['query']):
                        df = M.metric_run(metric,query)
                        if df.empty:
                            M.lib.log("WARNING","main",f"The metric {metric_file} query ({i}) returned an empty dataset.")
                        else:
                            df_metric = pd.concat([df_metric, df], ignore_index=True)
                
                    if df_metric.empty:
                            M.lib.log("ERROR","main",f"The metric {metric_file} had no data returned.  It will not be counted.",True)
                    df_detail = pd.concat([df_detail, df_metric], ignore_index=True)
                else:
                    M.lib.log("WARNING","main",f"No query found in {metric_file}.yml.  It will not be counted.")
    if df_detail.empty:
        M.lib.log("ERROR","main","The detail dataframe is empty - are you sure the metrics ran ok?",alert)
        exit(1)

    # == This is just cosmetic, to show the resulting scores on the screen, so developers can see the results of their work
    summary = df_detail.groupby('metric_id')['compliance'].agg(['sum', 'count']).reset_index()
    summary.columns = ['metric_id', 'totalok', 'total']
    summary['score'] = round(summary['totalok'] / summary['total'] * 100,2)
    print("")
    print(tabulate.tabulate(summary,headers="keys",showindex=False))
    print("")

    # == save the data file to be used by the publish process
    M.lib.log("INFO","main","Saving the detail data to parquet")
    try:
        df_detail.to_parquet(f"{KW['parquet']}")
        M.lib.log("SUCCESS","main",f"Detail data saved to {KW['parquet']}")
    except Exception as e:
        M.lib.log("ERROR","main",f"Failed to save the detail data to {KW['parquet']}: {e}",alert)

    M.lib.log("SUCCESS","main","Metric generation completed",alert)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Cyber Dashboard - Metric Generation')
    parser.add_argument('-dryrun', help='Runs the metrics for testing purposes', action='store_true')
    parser.add_argument('-metric',help='Run a dry-run test against a single metric')
    parser.add_argument('-path',help='The path where the metric yaml files are stored',default='.')
    parser.add_argument('-data',help='The path where the collector saves its files',default=os.environ.get('STORE_FILE','../data/source'))
    parser.add_argument('-privacy_off', help='Disables privacy mode', action='store_true', default=False)
    parser.add_argument('-parquet',help='The path where the metrics saves the resulting parquet file',default='../data/detail.parquet')

    args = parser.parse_args()

    main(
        metric_path     = args.path,
        data_path       = args.data,
        dryrun          = args.dryrun,
        metric          = args.metric,
        privacy         = not args.privacy_off,
        parquet         = args.parquet
    )
