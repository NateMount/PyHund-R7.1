
from sys import argv, exit
import yaml

# TODO: Add plugin support for custom output post-processing and handling
STDOUT_FORMATS = ['default', 'json', 'txt', 'pipe', 'csv', '_']

def display_help() -> None:
    help_text = """
[PyHund:Help ~]::

Usage: python3 pyhund.py <username1> <username2> ... [options]

Options (prefix with - or /):
\th | help\t\tDisplay this help message
\tstdin:<path>\t\tSpecify a file containing usernames (default: None)
\tstdout:<format>\t\tSpecify output format (default[stdout], json, txt, pipe)
\toutput_path:<path>\tSpecify output file path (default: pyhund_scan_results.<format>)
\tverbose\t\t\tEnable verbose output (only for stdout=default)
\tdebug\t\t\tEnable debug output (only for stdout=default/txt)
\tplugin-config:<config>\tSpecify plugin configuration in the format ( plugin=setting1,setting2+plugin2=setting3 )
    """
    print(help_text)
    exit(0)

def parse_args() -> dict:
    """
    Parse provided command line arguments into a configuration hash map
    :return: Hash map containing all parsed configuration options
    :rtype: dict
    """

    if len(argv) < 2: display_help()

    parsed_config = {
        "unames": [],
        "stdout": "default",
        "verbose": False,
        "debug": False,
        "plugin-config": ""
    }

    static_config_data = yaml.safe_load(open('/home/xxi/Projects/In-Progress/Tools/PyHund-R7.1/src/resources/config.yaml', 'r'))
    
    # If configurations were implemented in static config for the user then apply them prior to command line arguments
    if static_config_data['BaseConfig']:
        for key in static_config_data['BaseConfig'].keys():
            parsed_config[key] = static_config_data['BaseConfig'][key]
    
    # Parsing command line arguments
    for arg in argv[1:]:

        # If current arg is a flag or option then process that flag/option
        if arg.startswith('-') or arg.startswith('/'):
            arg = arg.lstrip('-').lstrip('/')

            # If requesting help then display and exit
            if arg.split(':')[0] in ('h', 'help'): display_help()

            if arg.split(':')[0] != "unames":
                parsed_config[arg.split(':')[0]] = arg.split(':')[1] if ':' in arg else True
            
            continue
        
        parsed_config['unames'].append(arg.strip())

    # Updating plugin config if configuration is provided
    parsed_config['plugin-config'] = {k.split('=')[0]: k.split('=')[1].split(',') for k in parsed_config['plugin-config'].split('+') if '=' in k}

    # If user has provided stdin option then read usernames from the specified file
    if 'stdin' in parsed_config.keys():
        try:
            with open(parsed_config['stdin'], 'r') as f:
                [ parsed_config['unames'].append(name.strip()) for name in f.read().split('\n') if name.strip() and not name.startswith('#') ]
        except FileNotFoundError:
            # Program will attempt to continue executing with usernames provided from command line arguments
            print(f"[Warn ~]:: File '{parsed_config['stdin']}' not found, please provide a valid file path, defaulting to unames from command line arguments")

    # If no usernames are provided, no operations can be performed, so exit
    if len(parsed_config['unames']) == 0:
        print("[Err ~]:: Must provide at least one username")
        exit(1)

    # If user has provided unknown stdout format then warn of improper option provided and run with stdout=default
    if parsed_config['stdout'] not in STDOUT_FORMATS:
        print('[Warn ~]:: Invalid output format specified, must be one of (default, json, txt, pipe, csv)\n           Reverting to default and continuing')
        parsed_config['stdout'] = 'default'

    return parsed_config