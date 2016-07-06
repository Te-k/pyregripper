#! /usr/bin/env python
from plugins.base import Plugin
from Registry import *

class PluginRecentDocs(Plugin):
    name = "recentdocs"
    htype = ["NTUSER"]
    description = "List windows recent docs"
    KEY = 'Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs'

    def run(self, registry, verbose, params={}):
        res = {}
        try:
            recent = registry.open(self.KEY)
        except:
            return res

        res['All Files'] = []
        for val in recent.values():
            res['All Files'].append(val.value().split('\x00\x00')[0])

        res['subkeys'] = {}
        for key in recent.subkeys():
            k = {'timestamp':  key.timestamp().strftime('%Y%m%d %H:%M:%S'),
                    'values': []}
            for val in key.values():
                if val.name() != 'MRUListEx':
                    k['values'].append(val.value().split('\x00\x00')[0])
            res['subkeys'][key.name()] = k

        return res


    def display_text(self, res, verbose):
        print('------------------------ Recent Docs ------------------------')
        if res == {}:
            print('No recent doc key on this hive.')
        else:
            # All Files
            print('\nAll Files')
            for entry in res['All Files']:
                print('\t-%s' % entry)

            # Subkeys
            for ttype in res['subkeys'].keys():
                print('\n%s' % ttype)
                print('\tLast Write Time: %s' % res['subkeys'][ttype]['timestamp'])
                for entry in res['subkeys'][ttype]['values']:
                    print('\t-%s' % entry)
