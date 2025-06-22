# [PyHund-R7.1:Plugin-Support-Module ~]
# This module includes the source 'Plugin' class, from which all 
# PyHund plugins must be children of in order to function

class Plugin:

    def __init__(self, plugin_name:str):
        self.plugin_name:str = plugin_name

    def handle_stdout(self, stdout_flag:str, scan_object:dict) -> None:
        """
        Handle Stdout
        This method is called when a passed in flag for stdout does not match any predefined methods 
        in the core of PyHund. This method is to be implemented by plugins that want the ability to 
        perform special stdout formats or preprocessing.
        :param stdout_flag: String represented flag that indicates what format the program output should be in
        :param scan_object: Dictionary containing the results of the scan
        :return: None, this should not return any data
        """
        return None
    
    def __repr__(self) -> str:
        return f"{self.plugin_name}"