# [PyHund-R7.1:init ~]
# Initialization file for the PyHund package.

# Imports
from pyhund.argparse import parse_args
from pyhund.scanning import run_scan
from pyhund.plugin_manager import PluginManager
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

    plugin_manager = PluginManager(config=config)

    # Test internet connection prior to execution
    if not check_internet_conn():
        print("[Err ~]: No internet connection found, aborting")
        exit(1)

    # Run the scan with the provided configuration
    scan_object:dict[str, dict[str, list]] = run_scan(config=config, plugin_manager=plugin_manager)

    # Iterate through the plugins and call their post_scan method if it exists
    # This allows plugins to modify the scan object after the scan has completed
    # and before the output is handled
    for plugin in plugin_manager.plugins_index:
        scan_object = plugin.post_scan(scan_object=scan_object)
    # Handle the scan output based on the configuration
    handle_scan_output(scan_object, config, plugin_manager)