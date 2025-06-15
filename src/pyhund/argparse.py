
from sys import argv, exit

def display_help() -> None:
    help_text = """
    """
    print(help_text)
    exit(0)

def parse_args() -> dict:

    if len(argv) < 2:
        display_help()

    parsed_config = {
        "unames": [],
        "stdout": "default",
    }
    
    for arg in argv[1:]:
        if arg.startswith('-') or arg.startswith('/'):
            arg = arg.lstrip('-').lstrip('/')

            if arg.split(':')[0] in ('h', 'help'):
                display_help()

            if arg.split(':')[0] in parsed_config.keys() and arg.split(':')[0] != "unames":
                parsed_config[arg.split(':')[0]] = arg.split(':')[1] if ':' in arg else None
        
        parsed_config['unames'].append(arg.strip)

    if not parsed_config['unames']:
        print("[Err ~]:: Must provide at least one username")
        exit(1)

    if parsed_config['stdout'] not in ['default', 'json', 'txt', 'pipe']:
        print('[Warn ~]:: Invalid output format specified, must be one of (default, json, txt, pipe)\n           Reverting to default and continuing')
        parsed_config['stdout'] = 'default'
    
    return parsed_config