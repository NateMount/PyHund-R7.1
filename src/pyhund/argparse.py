
from sys import argv, exit

def display_help() -> None:
    help_text = """
[PyHund:Help ~]::

Usage: python3 pyhund.py <username1> <username2> ... [options]

Options (prefix with - or /):
\th | help\t\tDisplay this help message
\tstdout:<format>\t\tSpecify output format (default[stdout], json, txt, pipe)
\tverbose\t\t\tEnable verbose output (only for stdout=default)
\tdebug\t\t\tEnable debug output (only for stdout=default/txt)
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
    }
    
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

    # If no usernames are provided, no operations can be performed, so exit
    if len(parsed_config['unames']) == 0:
        print("[Err ~]:: Must provide at least one username")
        exit(1)

    # If user has provided unknown stdout format then warn of improper option provided and run with stdout=default
    if parsed_config['stdout'] not in ['default', 'json', 'txt', 'pipe', 'csv', '_']:
        print('[Warn ~]:: Invalid output format specified, must be one of (default, json, txt, pipe, csv)\n           Reverting to default and continuing')
        parsed_config['stdout'] = 'default'

    return parsed_config