# Writing a collector

A collector is a small Python script responsible for connecting to a remote data source, and downloading the data.  The basic structure of a collector is as follow

* Environment variables are used to drive the collector
* Where possible, use the native SDK provided by the vendor.  When all else fails, resort to using [requests](https://pypi.org/project/requests/)
* Each collector has a `meta` section, that contains some basic information about the collector.
* Each collector utilises the [collector](../01-collectors/collector.py) class, which contains basic functions to handle data once it has been collected.

## Name it

The collector must be stored in the `01-collectors` folder, with the naming of `src_<name>.py`.

## Initilise the collector

Use the following boilerplate to get started

```python
from collector import Collector
from dotenv import load_dotenv
import requests

def get_data(C):
    data = []   # initialize an empty list.  It will contain all the records

    # -- do your extraction.
    req = requests.get('https://api.example.com/data.json',headers = { 'Authorization' : f"Bearer {os.environ['PLUGIN_SECRET']}"})
    if req.status_code == 200:
        data += req.json()
    
    # -- send the data to the storage function.  Name the tag as plugin_function
    C.store('plugin_getdata',data)

def meta():
    return {
        'plugin' : 'plugin_name',               # replace this with a short code for the collector
        'title'  : 'My fancy plugin',           # Replace this with a more descriptive name for the plugin
        'link'  : 'https://www.example.com/',   # Provide a URL to the SDK being used, or the API documentation
        'functions' : [ 'get_data','....'],     # Provide the list of functions that can be called.  This is only used to generate documentation
        'env' : {
            'PLUGIN_CLIENT_ID' : None,          # Provide any environment variables that will be used by the plugin.
            'PLUGIN_SECRET'    : None           # NOTE : they must be unique across all plugins, so prefix them with the name of the plugin
        }
    }

def main():
    C = Collector(meta())
    if C.test_environment():                    # Check if the environment variables are set.  If they are, we continue with the data retrieval
        get_data(C)                             # Call the function to retrieve the data

if __name__ == '__main__':
    load_dotenv()
    main()
```

## Adjust the code

The `get_data` function is an example of how you can extract data, and pass it to the collector.  You need to cater for thing like

* Unable to connect
* Invalid credentials
* Timeouts
* Rate limits

If you are using any additional modules, adjust the [requirements.txt](../requirements.txt) file accordingly.
