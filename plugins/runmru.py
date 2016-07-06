#! /usr/bin/env python
from plugins.base import Plugin
from Registry import *


class PluginTunmru(Plugin):
    name = "runmru"
    htype = ["NTUSER"]
    description = "List Explorer Run MRU entries"

    KEY = 'Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU'

    def run(self, registry, verbose, params={}):
        results = {}
        try:
            entry = registry.open(self.KEY)
        except Registry.RegistryKeyNotFoundException:
            return results
        results['entries'] = []
        for e in entry.values():
            results['entries'].append([e.name(), e.value()])
        results['timestamp'] = entry.timestamp().strftime('%d/%m/%Y %H:%M:%S')

        return results

    def display_text(self, results, verbose):
        print('------------------------ Run MRU ------------------------')
        print(self.KEY)
        print('')
        if results == {}:
            print('Registry key not found')
        else:
            print('Last Write Time: %s' % results['timestamp'])
            for entry in results['entries']:
                print("%s -> %s" % (entry[0], entry[1]))

    def display_csv(self, results, verbose):
        if results == []:
            print('Registry key not found')
        else:
            print("id|value")
            for entry in results['entries']:
                print("%s|%s" % (entry[0], entry[1]))


