#! /usr/bin/env python
from plugins.base import Plugin
from Registry import *

class PluginWordWhellQuery(Plugin):
    name = "wordwheelquery"
    htype = ["NTUSER"]
    description = "Get Windows search list in wordwheelquery entry"
    KEY = 'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\WordWheelQuery'

    def run(self, registry, verbose, params={}):
        res = {}
        try:
            key = registry.open(self.KEY)
            res['timestamp'] = key.timestamp().strftime('%Y%m%d %H:%M:%S')
            res['values'] = {}
            for val in key.values():
                if val.name() != 'MRUListEx':
                    res['values'][int(val.name())] = unicode(val.value(), encoding="latin-1", errors='replace')
        except Registry.RegistryKeyNotFoundException:
            pass

        return res

    def display_text(self, res, verbose):
        print("------------------ Word Wheel Query --------------------")
        if res == {}:
            print('No such key')
        else:
            print('Last Write Time: %s' % res['timestamp'])
            for k in sorted(res['values'].keys()):
                print("\t- %s: %s" % (k, res['values'][k]))

