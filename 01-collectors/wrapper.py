import os
import importlib
from dotenv import load_dotenv
import sys
sys.path.append('../')
from library import Library
import logging

def main():
    lib = Library()
    logging.info("Starting the collection process")
    lib.alert("INFO", "Starting the collection process")
    for filename in os.listdir('.'):
        if filename.startswith('src') and filename.endswith('.py'):
            plugin = os.path.splitext(filename)[0]
            logging.info(f"Plugin : {plugin}")

            try:
                module = importlib.import_module(plugin)
                m = module.meta()
                logging.info(m['title'])
                module.main()
            except ModuleNotFoundError:
                logging.warning(f"Plugin '{plugin}' not found.")
            except Exception as e:
                logging.error(f"Plugin '{plugin}' had an error {e}")
                lib.alert("ERROR", f"Plugin '{plugin}' had an error {e}")
    
    logging.info("Completed with the collection process")
    lib.alert("SUCCESS", "Completed with the collection process")
if __name__=='__main__':
    load_dotenv()
    main()