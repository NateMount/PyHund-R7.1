
from json import dump

def handle_scan_output(scan_object:object, config:dict) -> None:
    
    out_path = config.get('output_path', 'pyhund_scan_results.{}'.format(config['stdout'].lower()))

    match config['stdout'].lower():
        case "json":

            # Json Dump of Raw Scan Object
            dump(scan_object, open(out_path, 'w'))

        case "csv":
            with open(out_path, 'w') as f:

                # Writing header for CSV file
                # Format: username, sitename, url, response_code, validation_status, validation_method, hit_status
                f.write("username, sitename, url, response_code, validation_status, validation_method, hit_status\n")

                [
                    [ 
                        f.write("{}, {}, {}, {}, {}, {}, {}\n".format(uname,*result[0:6])) for result in scan_object['Results'][uname] 
                    ] for uname in scan_object['Results'] 
                ]
        case "txt":
            with open(out_path, 'w') as f:
                f.write("[PyHund:Scan ~]:: Scan Results\n\n")

                #Writing Metadata
                f.write("[Meta ~]:: \n")
                f.write("Total Hits: {}\nTotal Misses: {}\nTotal Unknown: {}\nTotal Visited: {}\n\n".format(*scan_object['Meta']))

                # Writing Results
                f.write("[Results ~]:: \n")
                for uname in scan_object['Results']:
                    f.write(f"[{uname} ~]:: \n")
                    [ 
                        f.write("Sitename: {}\nURL: {}\nResponse Code: {}\nValidation Status: {}\nValidation Method: {}\nHit Status: {}\n\n".format(*result)) 
                        for result in scan_object['Results'][uname] 
                    ]

        case "pipe":
            print("[Meta ~]:: HITS({}), MISSES({}), UNKNOWN({}), VISITED({})\n".format(*scan_object['Meta']))
            for uname in scan_object['Results']:
                [ 
                    print("Username({}), Sitename({}), URL({}), Response Code({}), Validation Status({}), Validation Method({}), Target Status({})".format(uname, *site[0:6])) 
                    for site in scan_object['Results'][uname] 
                ]

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
                    print("Sitename: {}\nURL: {}\nResponse Code: {}\nValidation Status: {}\nValidation Method: {}\nHit Status: {}\n".format(*result)) 
                    for result in scan_object['Results'][uname]
                ]

        case _:

            # TODO: Add plugin support for custom output post-processing and handling
            # Initial plugin concept
            [
                module.handle_stdout(config['stdout'].lower(), scan_object) for module in ()
            ]

            print("[Error ~]:: Unsupported output format specified in config.")
            return None