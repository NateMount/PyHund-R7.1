
from socket import create_connection
from json import load
from os.path import abspath
from sys import exit

MANIFEST_PATH:str = abspath(__file__).split('/pyhund')[0]+"/resources/site_manifest.json"

def check_internet_conn(refernce_bundle:tuple[str,int] = ('8.8.8.8',53), timeout:int = 5):
    """
    Check Internet Connection
    Used to ensure a stable connection prior to attempting to run scans
    :param config: Configuration object
    """
    
    try:
        create_connection(refernce_bundle, timeout=timeout)
        return True
    except OSError:
        return False

def load_maifest(config:dict) -> tuple[dict, list[dict]]:
    """
    Load Manifest
    Used to load the site manifest and parse it into usable components.
    :param config: Config object used to check for user defined manifest
    :return: Tuple containing manifest metadata and the array of hashmaps for each site
    :rtype: tuple(dict, list(dict))
    """

    try:
        data:dict = load(open(config['manifest'],'r'))
    except (KeyError, FileNotFoundError):
        data:dict = load(open(MANIFEST_PATH, 'r'))
    
    return data['SiteIndex'], data['Meta']

def display_help() -> None:
    """
    Used to display the help message for the program
    """
    print("""
[PyHund:Help ~]::

Usage: pyhund <username1> <username2> ... [options]
          
Options (prefix with - or /):
          
    Basic Options:
        help\t\t\tDisplay this help message
        verbose\t\t\tEnable verbose output (Should not be used with stdout=pipe)
        debug\t\t\tEnable debug output 
        noerr\t\t\tDisable any responses found to be Invalid or Miss
    
    Input/Output Options:
        stdin:<path>\t\tSpecify a file containing usernames (default: None)
        stdout:<format>\t\tSpecify output format (default[stdout], json, txt, pipe)
        output_path:<path>\tSpecify output file path (default: pyhund_scan_results.<format>)
    
    Runtime Options:
        manifest:<path>\t\tSpecify a custom manifest file (default: resources/site_manifest.json)
        flags:<flags>\t\tSpecify site flags to filter sites (e.g., "social,finance")
    
    Plugin Options:
        plugin-config:<config>\tSpecify plugin configuration in the format ( plugin=setting1,setting2+plugin2=setting3 )

    """)
    exit(0)