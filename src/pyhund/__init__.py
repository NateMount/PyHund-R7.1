
from pyhund.argparse import parse_args

def run():
    
    config = parse_args()

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