import os
import sys
import json
from Registry import *

class Plugin(object):
    def find_current(self, reg):
        '''Find the current control set'''
        select = reg.open('Select')
        current = select.value('Current').value()
        return "ControlSet%03i" % current

    def display(self, results, format, verbose):
        getattr(self, 'display_' + format)(results, verbose)

    def display_text(self, results, verbose):
        print("The plugin %s does not implement text output" % self.__class__.__name__)

    def display_json(self, results, verbose):
        """Return json format of results"""
        print(json.dumps(results))

    def display_csv(self, results, verbose):
        print("The plugin %s does not implement CSV output" % self.__class__.__name__)

def init_plugins():
    '''simple plugin initializer
    '''
    find_plugins()
    return register_plugins()

def find_plugins():
    '''find all files in the plugin directory and imports them'''
    plugin_dir = os.path.dirname(os.path.realpath(__file__))
    plugin_files = [x[:-3] for x in os.listdir(plugin_dir) if x.endswith(".py")]
    sys.path.insert(0, plugin_dir)
    for plugin in plugin_files:
        mod = __import__(plugin)

def register_plugins():
    '''Register all class based plugins.

        Uses the fact that a class knows about all of its subclasses
        to automatically initialize the relevant plugins
    '''
    PLUGINS = {}
    for plugin in Plugin.__subclasses__():
        PLUGINS[plugin.name] = plugin
    return PLUGINS
