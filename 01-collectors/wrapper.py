import os
import importlib
from dotenv import load_dotenv
import sys
sys.path.append('../')
from library import Library

def main():
    lib = Library()
    lib.log("INFO","wrapper","Starting the collection process",True)
    for filename in os.listdir('.'):
        if filename.startswith('src') and filename.endswith('.py'):
            plugin = os.path.splitext(filename)[0]
            lib.log("INFO","wrapper",f"Plugin : {plugin}")

            try:
                module = importlib.import_module(plugin)
                m = module.meta()
                lib.log("INFO","wrapper",m['title'])
                module.main()
            except ModuleNotFoundError:
                lib.log("WARNING","wrapper",f"Plugin '{plugin}' not found.")
            except Exception as e:
                lib.log("ERROR","wrapper",f"Plugin '{plugin}' had an error {e}",True)
    
    lib.log("SUCCESS","wrapper","Completed with the collection process",True)
if __name__=='__main__':
    load_dotenv()
    main()