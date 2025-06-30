from plugins import Plugin 

from yaml import dump as yaml_dump

# Basic YAML plugin for PyHund
# This plugin is a simple demo for basic plugin structure and functionality
# This is by all means not a great implementation of YAML handling, but serves as a basic example
# for how to implement a plugin in PyHund.
class YamlPlugin(Plugin):

    def __init__(self, config:dict, **kwargs):

        # Name of the plugin should be passed in as a string
        super().__init__("Yaml", config=config)

    def handle_stdout(self, stdout_flag, scan_object):

        # Check to see if output format is YAML
        if stdout_flag.lower() != "yaml":
            return None
        
        yaml_dump(scan_object, open(self.config.get('output_path', 'pyhund_scan_results.yaml'), 'w'), default_flow_style=False)
        
