from os import listdir
from plugins import Plugin
class PluginManager:

    def __init__(self, config:dict):
        self.config:dict = config
        self.plugins_index:list[Plugin] = []

        # Load plugins on initialization
        self.load_plugins()

    def load_plugins(self) -> None:
        """
        Load Plugins
        This function locates and loads all plugins from the 'src/plugins' directory.
        """

        # Iterate through the plugin index and import each plugin
        for plugin in listdir('/home/xxi/Projects/In-Progress/Tools/PyHund-R7.1/src/plugins'):

            # Fast rejection of non-Python files and __* files
            if not plugin.endswith('.py') or plugin.startswith('__'):
                continue

            if ( module := self._load_plugin(plugin)) is not None:
                self.plugins_index.append(module(config=self.config))


    def _load_plugin(self, plugin_name:str) -> Plugin:
        """
        Load Plugin <Private>
        This function attempts to import a single plugin based on its name ( case sensitive ).
        :param plugin_name: The name of the plugin to load, must be a valid Python file in the plugins directory.
        :return: An instance of the plugin class if successful, None otherwise.
        """

        try:

            # If debugging or verbose mode is enabled, print the plugin being loaded
            self._log(f"Loading plugin {plugin_name[:-3]}...")

            # Attempt to get the plugin class "<Plugin_Name>Plugin" from module "<Plugin_Name>"
            return getattr(
                    getattr(__import__(
                        "plugins.{}".format(plugin_name[:-3])), 
                        plugin_name[:-3]
                    ), 
                    plugin_name[:-3] + "Plugin"
                )
        
        # If module cannot be imported, catch the ImportError
        # Report the error if debugging or verbose mode is enabled
        except ImportError as e:

            self._error(f"Failed to import plugin {plugin_name[:-3]}: {e}")
            return None
        
    def _log(self, message:str) -> None:
        if self.config['debug'] or self.config['verbose']:
            print(f"[PyHund:PluginManager ~]:: {message}")
    
    def _error(self, message:str) -> None:
        if self.config['debug'] or self.config['verbose']:
            print(f"[PyHund:PluginManager:Err ~]:: {message}")
