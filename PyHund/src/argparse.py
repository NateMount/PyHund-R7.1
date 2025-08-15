# [PyHund/ArgParse ~]
# Argument parser for PyHund

# === Imports
from sys import argv, exit
from yaml import safe_load
from os.path import abspath

from src.util import display_help, get_version

# === Functions
def parse_args() -> dict:
    """
    Parse Args
    Parse provided command line arguments into a configuration hash map
    :return: Hash map containing all parsed configuration options
    :rtype: dict
    """

    # If not enough arguments provided then display help and exit
    if len(argv) < 2: display_help()

    # Initializing parsed config file with necessary defaults
    parsed_config = {
        "unames": [],
        "stdout": "default",
        "verbose": False,
        "debug": False,
        "plugin-config": ""
    }

    # Load in static configuration data from config.yaml file
    static_config_data = safe_load(open(abspath(__file__).split('/src')[0]+'/resources/config.yaml', 'r'))
    
    # If configurations were implemented in static config for the user then apply them prior to command line arguments
    if static_config_data['BaseConfig']:
        parsed_config.update(static_config_data['BaseConfig'])
    
    # Parsing command line arguments
    for arg in argv[1:]:

        # If current arg is a flag or option then process that flag/option
        if arg.startswith('-') or arg.startswith('/'):
            arg = arg.lstrip('-').lstrip('/')

            # If requesting help then display and exit
            if arg.split(':')[0] == "help": display_help()

            if arg.split(':')[0] == "version":
                print(get_version())
                exit(0)

            # Do not allow users to attempt to set unames via options, only via command line arguments
            if arg.split(':')[0] != "unames":
                parsed_config[arg.split(':')[0]] = arg.split(':')[1:] if ':' in arg else True
            
            continue
        
        # If not an option then treat it as a username
        parsed_config['unames'].append(arg.strip())

    # Implement Plugin Configs from static config file
    if static_config_data['PluginConfig']:
        [ parsed_config['plugin-config'].update({plugin: static_config_data['PluginConfig'][plugin]}) for plugin in static_config_data['PluginConfig'] ]

    # Updating plugin config if configuration is provided
    parsed_config['plugin-config'] = {k.split('=')[0]: k.split('=')[1].split(',') for k in parsed_config['plugin-config'].split('+') if '=' in k}

    # If user has provided stdin option then read usernames from the specified file
    if 'stdin' in parsed_config.keys():
        try:
            with open(parsed_config['stdin'], 'r') as f:
                [ parsed_config['unames'].append(name.strip()) for name in f.read().split('\n') if name.strip() and not name.startswith('#') ]
        except FileNotFoundError:
            # Program will attempt to continue executing with usernames provided from command line arguments
            print(f"[PyHund:Warn ~]:: File '{parsed_config['stdin']}' not found, please provide a valid file path, defaulting to unames from command line arguments")

    # If no usernames are provided, no operations can be performed, so exit
    if len(parsed_config['unames']) == 0:
        print("[PyHund:Err ~]:: Must provide at least one username")
        exit(1)

    return parsed_config