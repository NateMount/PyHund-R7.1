
from socket import create_connection

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

