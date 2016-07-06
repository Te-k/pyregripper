#! /usr/bin/env python
from plugins.base import Plugin
from Registry import *


class PluginTypedurls(Plugin):
    name = "typedurls"
    htype = ["NTUSER"]
    description = "List urls typed in Internet Explorer bar"

    KEY = 'Software\Microsoft\Internet Explorer\TypedURLs'

    def run(self, registry, verbose, params={}):
        results = {}
        try:
            urls = registry.open(self.KEY)
        except Registry.RegistryKeyNotFoundException:
            return results
        results['urls'] = []
        for url in urls.values():
            results['urls'].append([url.name(), url.value()])
        results['timestamp'] = urls.timestamp().strftime('%d/%m/%Y %H:%M:%S')

        return results

    def display_text(self, results, verbose):
        print('------------------------ Typed URLs ------------------------')
        print(self.KEY)
        print('')
        if results == {}:
            print('Registry key not found')
        else:
            print('Last Write Time: %s' % results['timestamp'])
            for entry in results['urls']:
                print("%s -> %s" % (entry[0], entry[1]))

    def display_csv(self, results, verbose):
        if results == []:
            print('Registry key not found')
        else:
            print("id|url")
            for entry in results['urls']:
                print("%s|%s" % (entry[0], entry[1]))


