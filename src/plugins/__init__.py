# [PyHund-R7.1:Plugin-Support-Module ~]
# This module includes the source 'Plugin' class, from which all 
# PyHund plugins must be children of in order to function

class Plugin:

    def __init__(self, plugin_name:str, config:dict):
        self.plugin_name:str = plugin_name
        self.config:dict = config

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
    
    def post_scan(self, scan_object:dict) -> None:
        """
        Post Scan
        This method is called after the scan has completed. It can be used to perform any post-scan processing.
        :param scan_object: Dictionary containing the results of the scan
        :param config: Configuration dictionary passed to the plugin manager
        :return: scan_object: The scan object after any modifications made by the plugin
                 If no modifications are made, the original scan_object is returned
        """
        return scan_object
    
    def  handle_scan(self, scan_results:list) -> dict:
        """
        Handle Scan
        This method is called during the scan process. It can be used to perform any scan result processing.
        :param scan_object: Dictionary containing the results of the scan
        :param config: Configuration dictionary passed to the plugin manager
        :return: scan_object: The scan object after any modifications made by the plugin
                 If no modifications are made, the original scan_object is returned
        """
        return scan_results
    
    def __repr__(self) -> str:
        return f"{self.plugin_name}"