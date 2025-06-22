
from socket import create_connection
from json import load
from os.path import abspath

MANIFEST_PATH:str = abspath(__file__).split('/pyhund')[0]+"/resources/site_manifest.json"

def check_internet_conn(config:dict, refernce_bundle:tuple[str,int] = ('8.8.8.8',53), timeout:int = 5):
    """
    Check Internet Connection
    Used to ensure a stable connection prior to attempting to run scans
    :param config: Configuration object
    """

    if config['verbose'] == True:
        print("[PyHund:Pre-Check ~]:: Checking Internet Connection...")
    
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
