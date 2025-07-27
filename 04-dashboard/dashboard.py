import pandas as pd
import http.server
import socketserver
import os
import sys
from pathlib import Path

def convert(input_path, output_path):
    """Convert parquet files to JSON for dashboard consumption"""
    # TODO - we may need to do slicing here....
    for x in ['summary','detail']:
        parquet_file = f"{input_path}/{x}.parquet"
        json_file = f"{output_path}/{x}.json"
        
        if os.path.exists(parquet_file):
            df = pd.read_parquet(parquet_file)
            df.to_json(json_file, orient="records", indent=2)
            print(f"Converted {parquet_file} to {json_file}")
        else:
            print(f"Warning: {parquet_file} not found")

def start_server(port=8000, directory="src"):
    """Start HTTP server to serve dashboard files"""
    # Change to the directory containing the dashboard files
    os.chdir(directory)
    
    # Create HTTP server
    handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"Dashboard server started at http://localhost:{port}")
            print(f"Serving directory: {os.getcwd()}")
            print("Press Ctrl+C to stop the server")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"Port {port} is already in use. Try a different port.")
            sys.exit(1)
        else:
            raise

if __name__ == '__main__':
    # Convert data files
    convert('../data', 'src/json')
    
    # Start web server
    start_server()