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
import logging

class Metric:
    def __init__(self,**KW):
        self.lib = Library()
        
        if KW.get('data_path'):
            self.data_path = KW['data_path']
            logging.info(f"Data Path = {self.data_path}")
        else:
            logging.error("No data path specified")
            # Note: No alert possible here as lib is not available in __init__
            exit(1)
        
        self.datestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
        logging.info(f"Datestamp = {self.datestamp}")
        self.history = []
        self.data_tables = {}

    def resolve_ref(self, table_name):
        self.data_tables[table_name] = f"{self.data_path}/{table_name}/*.json"
        col = ''
        if table_name == 'crowdstrike_hosts':
            col = ",columns={'last_seen': 'VARCHAR','device_id' : 'VARCHAR','hostname' : 'VARCHAR'}"

        return f"read_json('{self.data_tables[table_name]}'{col})"
        
    def metric_run(self,yaml_config,query,alert=False):
        if yaml_config.get('enabled',True) == False or query == None:
            logging.info(f"Metric {yaml_config['metric_id']} is disabled")
            return pd.DataFrame()
        self.data_tables = {}
        env = Environment(loader=FileSystemLoader('.'))
        env.globals['ref'] = self.resolve_ref
        template = env.from_string(query).render()

        # == check if the tables defined in the SQL query actually exist
        success = True
        for table in self.data_tables:
            if len(glob.glob(self.data_tables[table])) > 0:
                logging.info(f"Table {table} exists")
            else:
                logging.error(f"Table {table} does not exist ({self.data_tables[table]})")
                if alert:
                    self.lib.alert("ERROR", f"Table {table} does not exist ({self.data_tables[table]})")
                success = False
        if not success:
            return pd.DataFrame()

        # == execute the query
        try:
            # Execute query
            df = duckdb.query(template).df()
            logging.info(f"Retrieved {len(df)} records")
            if args.dryrun:
                print(df)
        except duckdb.Error as e:
            logging.error(f"Failed to execute query: {e}")
            if alert:
                self.lib.alert("ERROR", f"Failed to execute query: {e}")
            print(template)
            return pd.DataFrame()
        
        # == check if the mandatory columns are there
        success = True
        for col in [ 'resource','resource_type','compliance','detail']:
            if not col in df.columns:
                logging.error(f" - Column {col} does not exists.  Check the SQL in your metric defintion")
                if alert:
                    self.lib.alert("ERROR", f"Column {col} does not exist. Check the SQL in your metric definition")
                success = False
        if not success:
            return pd.DataFrame()

        # == add the meta data
        success = True

        for f in ['metric_id','title','category','indicator','weight','type','description','how']:
            if f in yaml_config:
                df[f] = yaml_config[f]
            else:
                logging.error(f"{f} is missing in meta data")
                if alert:
                    self.lib.alert("ERROR", f"{f} is missing in meta data")
                success = False
        
        # Handle SLO - extract from array format
        if 'slo' in yaml_config and yaml_config['slo']:
            slo_values = yaml_config['slo']
            if isinstance(slo_values, list) and len(slo_values) > 0:
                df['slo_min'] = slo_values[0] if len(slo_values) > 0 else None
                df['slo'] = slo_values[1] if len(slo_values) > 1 else slo_values[0]
            else:
                df['slo'] = slo_values
                df['slo_min'] = slo_values
        else:
            df['slo'] = None
            df['slo_min'] = None
        
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
    lib = Library()
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
                logging.info("-----------------------------------------------------------------------")
                logging.info(f"Metric : {metric_file}")
                df_metric = pd.DataFrame()
                if 'query' in metric and metric['query'] != None:
                    for i,query in enumerate(metric['query']):
                        df = M.metric_run(metric,query,alert)
                        if df.empty:
                            logging.warning(f"The metric {metric_file} query ({i}) returned an empty dataset.")
                        else:
                            df_metric = pd.concat([df_metric, df], ignore_index=True)
                
                    if df_metric.empty:
                        logging.error(f"The metric {metric_file} had no data returned.  It will not be counted.")
                        if alert:
                            M.lib.alert("ERROR", f"The metric {metric_file} had no data returned.  It will not be counted.")
                    else:
                        if KW['metric'] != None:
                            print(df_metric)

                    df_detail = pd.concat([df_detail, df_metric], ignore_index=True)
                else:
                    logging.warning(f"No query found in {metric_file}.yml.  It will not be counted.")
    if df_detail.empty:
        logging.error("The detail dataframe is empty - are you sure the metrics ran ok?")
        if alert:
            M.lib.alert("ERROR", "The detail dataframe is empty - are you sure the metrics ran ok?")
        exit(1)

    # == This is just cosmetic, to show the resulting scores on the screen, so developers can see the results of their work
    summary = df_detail.groupby('metric_id')['compliance'].agg(['sum', 'count']).reset_index()
    summary.columns = ['metric_id', 'totalok', 'total']
    summary['score'] = round(summary['totalok'] / summary['total'] * 100,2)
    print("")
    print(tabulate.tabulate(summary,headers="keys",showindex=False))
    print("")

    # == save the data file to be used by the publish process
    logging.info("Saving the detail data to parquet")
    try:
        df_detail.to_parquet(f"{KW['parquet']}/detail.parquet")
        logging.info(f"Detail data saved to {KW['parquet']}/detail.parquet")
    except Exception as e:
        logging.error(f"Failed to save the detail data to {KW['parquet']}/detail.parquet: {e}")
        if alert:
            M.lib.alert("ERROR", f"Failed to save the detail data to {KW['parquet']}/detail.parquet: {e}")

    # -- backup the file to S3
    if 'STORE_AWS_S3_BUCKET' in os.environ:
        lib.upload_to_s3(f"{KW['parquet']}/detail.parquet",os.environ['STORE_AWS_S3_BUCKET'],'detail.parquet')

    # == pivot the summary
    primary_columns = ['datestamp','metric_id','title','category','slo','slo_min','weight','indicator']
    new_columns = [key for key in ['business_unit','team','location'] if key not in primary_columns]
    
    # Group by primary columns and count compliance
    df_summary = df_detail.groupby(primary_columns + new_columns).agg({'compliance' : ['sum','count']}).reset_index()
    df_summary.columns = primary_columns + new_columns + ['totalok', 'total']

    ## IMPORTANT ## 
    # before we merge the data, we need to check if the local parquet file already exists.  If it does, we won't be grabbing it from S3.
    if not os.path.exists(f"{KW['parquet']}/summary.parquet") and 'STORE_AWS_S3_BUCKET' in os.environ:
        lib.download_from_s3(os.environ['STORE_AWS_S3_BUCKET'],'summary.parquet',target = f"{KW['parquet']}/summary.parquet",parameter = None)

    if os.path.exists(f"{KW['parquet']}/summary.parquet"):
        orig_summary_df = pd.read_parquet(f"{KW['parquet']}/summary.parquet")

        # Ensure the columns exist in both DataFrames
        if 'metric_id' in orig_summary_df.columns and 'datestamp' in orig_summary_df.columns:
            # Get a set of metric_id and datestamp pairs to remove
            to_remove = set(zip(df_summary['metric_id'], df_summary['datestamp']))

            # Filter the original DataFrame to exclude rows matching any of the pairs
            orig_summary_df = orig_summary_df[
                ~orig_summary_df[['metric_id', 'datestamp']].apply(tuple, axis=1).isin(to_remove)
            ]

        # Concatenate the updated original DataFrame with the new summary
        df_summary = pd.concat([df_summary, orig_summary_df], ignore_index=True)

    df_summary['datestamp'] = pd.to_datetime(df_summary['datestamp'], errors='coerce')
    df_summary['datestamp'] = pd.to_datetime(df_summary['datestamp'], errors='coerce').dt.strftime('%Y-%m-%d')

    if 'indicator' not in df_summary.columns:
        df_summary['indicator'] = False
    df_summary['indicator'] = df_summary['indicator'].fillna('').astype(str).str.lower() == 'true'
    
    df_summary.to_parquet(f"{KW['parquet']}/summary.parquet", index=False)
    if 'STORE_AWS_S3_BUCKET' in os.environ:
        lib.upload_to_s3(f"{KW['parquet']}/summary.parquet",os.environ['STORE_AWS_S3_BUCKET'],'summary.parquet')

    logging.info("Metric generation completed")
    if alert:
        M.lib.alert("SUCCESS", "Metric generation completed")

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Cyber Dashboard - Metric Generation')
    parser.add_argument('-dryrun', help='Runs the metrics for testing purposes', action='store_true')
    parser.add_argument('-metric',help='Run a dry-run test against a single metric')
    parser.add_argument('-path',help='The path where the metric yaml files are stored',default='.')
    parser.add_argument('-data',help='The path where the collector saves its files',default=os.environ.get('STORE_FILE','../data/source'))
    parser.add_argument('-parquet',help='The path where the metrics saves the resulting parquet file',default='../data')

    args = parser.parse_args()

    main(
        metric_path     = args.path,
        data_path       = args.data,
        dryrun          = args.dryrun,
        metric          = args.metric,
        parquet         = args.parquet
    )
