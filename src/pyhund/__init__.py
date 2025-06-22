# [PyHund-R7.1:init ~]
# Initialization file for the PyHund package.

# Imports
from pyhund.argparse import parse_args
from pyhund.scanning import run_scan
from pyhund.output_handler import handle_scan_output
from pyhund.util import check_internet_conn, load_maifest

def run():
    
    # Derive configuration from command line arguments
    config:dict[str, any] = parse_args()

    # If verbose or debug mode active, display version and config info
    if config['verbose'] or config['debug']:
        print("\n[PyHund:Config ~]:: Configuration Data")
        print("---------------------------------------")
        [ print("{:<16}:\t {}".format(k.capitalize(), v)) for k, v in config.items() ]
        print("Manifest Version:\t {}".format(load_maifest(config=config)[1]['version']))

    # TODO: Add plugin support for custom configuration handling prior to scan execution

    # Test internet connection prior to execution
    if not check_internet_conn():
        print("[Err ~]: No internet connection found, aborting")
        exit(1)

    # Run the scan with the provided configuration
    scan_object:dict[str, dict[str, list]] = run_scan(config=config)

    # TODO: Add plugin support for custom post-scan processing
    
    # Handle the scan output based on the configuration
    handle_scan_output(scan_object, config)