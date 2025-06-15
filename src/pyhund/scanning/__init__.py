
from json import load
from os.path import abspath

# Load site manifest containing all sites to scan
site_manifest = load(open(abspath(".")+"/resources/site_manifest.json", "r"))
print(abspath("."))
# Unpack loaded data into usable 'SiteIndex' and 'Meta' components
site_index = site_manifest["SiteIndex"]
site_index_meta = site_manifest["Meta"]

def run_scan(config:dict) -> dict:
    """
    Initializes mass scan and returns a scan result object contaning metadata and results.
    :param config: Configuration hash map containing all passed in scanning parameters.
    :return: Hash map containing metadata and individual scan results.
    :rtype: dict
    """
    
    scan_results = {
        # Metadata on program run as a whole
        "Meta": [0,0,0,0], # [Total Hits, Total Misses, Total Unknown, Total Visited]
        
        # Results per username in the format as follows
        # [sitename, url, response_code, validation_status, validation_method, hit_status]
        #     # Sitename: Display name of the visited site
        #     # URL: URL used by the program to attempt to find the account and validate for authentication
        #     # Response Code: HTTP response code returned by the site
        #     # Validation Status: Status of validation on authenticity of site response (e.g., "Valid", "Invalid", "Unknown")
        #     # Validation Method: Method used to validate the response (e.g., "RegEx", "Status", "URL")
        #     # Hit Status: Status of the hit (e.g., "Hit", "Miss", "Unknown")
        "Results": {}
    }

    for uname in set(config['unames']):

        # Make a new user entry in the results object
        scan_results["Results"][uname.lower()] = []
    
    return scan_results