
from json import dump

def handle_scan_output(scan_object:object, config:dict) -> None:
    
    out_path = config.get('output_path', 'pyhund_scan_results.{}'.format(config['stdout'].lower()))

    match config['stdout'].lower():
        case "json":
            dump(scan_object, open(out_path, 'w'))
        case "csv":
            with open(out_path, 'w') as f:
                f.write("username, sitename, url, response_code, validation_status, validation_method, hit_status\n")
                for uname in scan_object['Results']:
                    for result in scan_object['Results'][uname]:
                        f.write("{}, {}, {}, {}, {}, {}, {}\n".format(uname,*result[0:6]))
        case "txt":
            pass
        case "pipe":
            pass
        case "default":
            pass
        case _:
            return None