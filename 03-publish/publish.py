import argparse
import pandas as pd
import os
import sys
from dotenv import load_dotenv
sys.path.append('../')
from library import Library
from sqlalchemy import create_engine, text
import requests

class Publish:
    def __init__(self,**KW):
        self.lib = Library()

    def upload_to_postgres(self,df, table_name, if_exists="replace"):
        DB_HOST = os.getenv("POSTGRES_HOST")
        DB_NAME = os.getenv("POSTGRES_DATABASE")
        DB_PORT = os.getenv("POSTGRES_PORT", "5432")  # Default to 5432 if not set
        DB_USER = os.getenv("POSTGRES_USER")
        DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        
        # Check that all required environment variables are set
        if not all([DB_HOST, DB_NAME, DB_USER, DB_PASSWORD]):
            self.lib.log("WARNING","upload_to_postgres","One or more PostgreSQL environment variables are not set.")
            return
        
        # Create a SQLAlchemy engine
        engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        
        self.lib.log("INFO","upload_to_postgres",f"Uploading {len(df)} records to the '{table_name}' table...")
        try:
            # Write the DataFrame to the PostgreSQL database
            df.to_sql(table_name, engine, if_exists=if_exists, index=False)
            self.lib.log("SUCCESS","upload_to_postgres",f"Data successfully uploaded to the '{table_name}' table.")
        except Exception as e:
            self.lib.log("ERROR","upload_to_postgres",f"Error uploading data to PostgreSQL: {e}")
            raise

    def run_sql_on_postgres(self,file_path):
        DB_HOST = os.getenv("POSTGRES_HOST")
        DB_NAME = os.getenv("POSTGRES_DATABASE")
        DB_PORT = os.getenv("POSTGRES_PORT", "5432")  # Default to 5432 if not set
        DB_USER = os.getenv("POSTGRES_USER")
        DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        
        # Check that all required environment variables are set
        if not all([DB_HOST, DB_NAME, DB_USER, DB_PASSWORD]):
            self.lib.log("WARNING","run_sql_on_postgres","One or more PostgreSQL environment variables are not set.")
            return
        try:
            engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",isolation_level="AUTOCOMMIT")
            self.lib.log("INFO","run_sql_on_postgres",f"Executing SQL script '{file_path}'...")
            # Connect to the database
            with engine.connect() as connection:
                # Read and execute the SQL file
                with open(file_path, 'r') as sql_file:
                    sql_statements = sql_file.read()
                    
                    # Split the SQL script into individual statements
                    for statement in sql_statements.split(";"):
                        statement = statement.strip()
                        if statement:
                            connection.execute(text(statement))
                self.lib.log("SUCCESS","run_sql_on_postgres","SQL script executed successfully.")
        
        except Exception as e:
            self.lib.log("ERROR","run_sql_on_postgres",f"Error executing SQL file: {e}",True)
        
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

    P.upload_to_postgres(df, "detail", if_exists="replace")
    P.run_sql_on_postgres("postgres_summary.sql")

    P.lib.log("INFO","main","All done")

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Cyber Dashboard - Publish metrics')
    parser.add_argument('-parquet',help='The path where the metrics saves the resulting parquet file',default='../data/detail.parquet')

    args = parser.parse_args()

    main(
        parquet         = args.parquet
    )