
from pyhund.argparse import parse_args
from pyhund.scanning import run_scan, site_index_meta
from pyhund.output_handler import handle_scan_output

def run():
    
    config = parse_args()

    # If verbose or debug mode active, display version and config info
    if config['verbose'] or config['debug']:
        print("\n[PyHund:Config ~]:: Configuration Data")
        print("---------------------------------------")
        for k, v in config.items():
            print("{:<16}:\t {}".format(k.capitalize(), v))
        print("Manifest Version:\t {}".format(site_index_meta['version']))

    scan_object = run_scan(config=config)
    
    handle_scan_output(scan_object, config)