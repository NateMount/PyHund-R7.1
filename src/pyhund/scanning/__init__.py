
from pyhund.util import load_maifest
from pyhund.scanning.scan_operations import scan_site_verify

def run_scan(config:dict) -> dict:
    """
    Initializes mass scan and returns a scan result object contaning metadata and results.
    :param config: Configuration hash map containing all passed in scanning parameters.
    :return: Hash map containing metadata and individual scan results.
    :rtype: dict
    """
    
    # Load specified manifest
    site_index, site_index_meta = load_maifest(config=config)

    scan_results = {
        # Metadata on program run as a whole
        "Meta": [0,0,0,0], # [Total Hits, Total Misses, Total Unknown, Total Visited]
        
        # Results per username in the format as follows
        # [sitename, url, response_code, validation_status, validation_method, hit_status]
        #      Sitename: Display name of the visited site
        #      URL: URL used by the program to attempt to find the account and validate for authentication
        #      Response Code: HTTP response code returned by the site
        #      Validation Status: Status of validation on authenticity of site response (e.g., "Valid", "Invalid", "Unknown")
        #      Validation Method: Method used to validate the response (e.g., "RegEx", "Status", "URL")
        #      Hit Status: Status of the hit (e.g., "Hit", "Miss", "Unknown")
        "Results": {}
    }

    for uname in set(config['unames']):

        # Make a new user entry in the results object
        scan_results["Results"][uname.lower()] = []

        # Print a message indicating the start of the scan for the current user
        if config['verbose'] or config['debug']:
            print(f"\n[PyHund:Scan ~]:: Scanning for user '{uname}'")

        # Iterate though each site in the site index and scan for the username
        for i, site in enumerate(site_index):
            
            # If site tags do not match the tags provided by the user then skip
            if 'flags' in config:
                if not set(config['flags'].split(',')).issubset(site['flags']): 
                    continue

            # Print current site number being scanned if verbose or debug mode is active
            if config['verbose']:
                print(f"[PyHund:Scan ~]({uname}):: Scanning site #({i + 1}/{site_index_meta['site_count']})", end="\r")

            # Scan and parse site data then add to results for current user
            result:list = scan_site_verify(site, uname)

            # If NoErr flag set then ignore any erronious responses
            if 'NoErr' in config.keys():
                if result[5] == "Miss" or result[3] == "Invalid":
                    continue
            
            # Increment total hits / misses / unknowns based on the result
            if result[5] == "Hit": scan_results["Meta"][0] += 1
            elif result[5] == "Miss": scan_results["Meta"][1] += 1
            if result[3] == "Unknown": scan_results["Meta"][2] += 1

            # Increment the total visited sites count
            scan_results["Meta"][3] += 1

            # TODO: Add plugin support for custom scan result processing and handling 

            # Append the result to the user's results
            scan_results["Results"][uname.lower()].append(result)
                
        # For verbose output, print a blank char to reset carriage return
        if config['verbose']: print("")
        
    return scan_results