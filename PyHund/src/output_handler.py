# [PyHund/OutputHandler ~]
# Handler for all output modes of PyHund

# === Imports
from json import dump

# === Functions
def handle_scan_output(scan_object:dict, config:dict, plugin_manager:object = None) -> None:
    """
    Handle Scan Output
    Used to determine the desired output mode for each run of PyHund and then execute the desired
    mode for stdout.
    :param scan_object: An object containing all prevelent scan data resulting from PyHund execution
    :param config: Config dict generated at run start to determine which mode to use and what params
                   to set for that mode.
    :param plugin_manager: PluginManager object used to handle any potential plugin calls for 
                           output [Default = None]
    """

    match config['stdout'].lower():

        # JSON
        case "json":
            # Json Dump of Raw Scan Object
            dump(scan_object, open(config.get('output_path', 'pyhund_scan_results.json'), 'w'))

        # CSV
        case "csv":
            with open(config.get('output_path', 'pyhund_scan_results.csv'), 'w') as f:

                # Writing header for CSV file
                f.write("username, sitename, url, response_code, validation_status, validation_method, hit_status\n")

                # Writing Results
                # Replace commas in the results with '&' to avoid CSV issues
                [[
                    f.write(f"{uname}, " + ", ".join([ 
                        x.replace(',', ' &') for x in map(str, result)
                    ]) + "\n") for result in scan_object['Results'][uname]
                ] for uname in scan_object['Results'] ]

        # Raw text option
        case "txt":
            with open(config.get('output_path', 'pyhund_scan_results.txt'), 'w') as f:
                f.write("[PyHund:Scan ~]:: Scan Results\n\n")

                #Writing Metadata
                f.write("[Meta ~]:: \n")
                f.write("Total Hits: {}\nTotal Misses: {}\nTotal Unknown: {}\nTotal Visited: {}\n\n".format(*scan_object['Meta']))

                # Writing Results
                f.write("[Results ~]:: \n")
                for uname in scan_object['Results']:
                    f.write(f"[{uname} ~]:: \n")
                    [ 
                        f.write("Sitename: {}\nURL: {}\nResponse Code: {}\nValidation Status: {}\nValidation Method: {}\nHit Status: {}\n\n".format(*result[0:6])) 
                        for result in scan_object['Results'][uname] 
                    ]

        #Pipe optimized output for '| grep' operations
        case "pipe":
            print("[Meta ~]:: HITS({}), MISSES({}), UNKNOWN({}), VISITED({})\n".format(*scan_object['Meta']))
            for uname in scan_object['Results']:
                [ 
                    print("Username({}), Sitename({}), URL({}), Response Code({}), Validation Status({}), Validation Method({}), Target Status({})".format(uname, *site[0:6])) 
                    for site in scan_object['Results'][uname] 
                ]

        # Basic STDOUT option
        case "default":
            print("[PyHund:Scan ~]:: Scan Results")

            # Print Metadata
            print("[Meta ~]::")
            print("Total Hits: {}\tTotal Misses: {}\tTotal Unknown: {}\tTotal Visited: {}\n\n".format(*scan_object['Meta']))

            # Print Results
            print("[Results ~]::\n")
            for uname in scan_object['Results']:
                print(f"[{uname} ~]::")
                [ 
                    print("Sitename: {}\nURL: {}\nResponse Code: {}\nValidation Status: {}\nValidation Method: {}\nHit Status: {}\n".format(*result[0:6])) 
                    for result in scan_object['Results'][uname]
                ]

        # If no other matches then check plugins for a match
        case _:

            [
                module.handle_stdout(config['stdout'].lower(), scan_object) for module in plugin_manager.plugins_index if 'disabled' not in module.settings # type: ignore
            ]