#! /usr/bin/env python
from plugins.base import Plugin
from Registry import *


class PluginWinevt(Plugin):
    name = "winevt"
    htype = ["SOFTWARE"]
    description = "Display logging policy settings"

    KEY = 'Microsoft\Windows\CurrentVersion\WINEVT\Channels'

    def run(self, registry, verbose, params={}):
        """Run the plugin"""
        results = []
        try:
            channels = registry.open(self.KEY)
        except Registry.RegistryKeyNotFoundException:
            return results
        for evt in channels.subkeys():
            results.append({'name': evt.name(),
                'write_time': evt.timestamp().strftime('%d/%m/%Y %H:%M:%S (UTC)'),
                'enabled': evt.value('Enabled').value(),
                'type': evt.value('Type').value()})

        return results

    def display_text(self, results, verbose):
        """Display results in console format"""
        print('------------------------ Win EVT ------------------------')
        if results == []:
            print('Registry key not found')
        else:
            for entry in results:
                print('Name\t\t: %s' % entry['name'])
                print('Enabled\t\t: %i' % entry['enabled'])
                print('Type\t\t: %i' % entry['type'])
                print('Last Write Time : %s' % entry['write_time'])
                print('')

