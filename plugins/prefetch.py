#! /usr/bin/env python
from plugins.base import Plugin
from Registry import *


class PluginPrefetch(Plugin):
    name = "prefetch"
    htype = ["SYSTEM"]
    description = "Display information on the prefetch configuration"

    VALUES = {
            0: 'Prefetching is disabled',
            1: 'Application prefetching is enabled',
            2: 'Boot prefetching is enabled',
            3: 'Both boot and application prefetching is enabled'
    }
    KEY = '\Control\Session Manager\Memory Management\PrefetchParameters'

    def run(self, registry, verbose, params={}):
        """Run the plugin"""
        results = {'success': True}
        try:
            currentset = self.find_current(registry)
        except:
            results['success'] = False
        try:
            pref = registry.open(currentset + self.KEY)
            results['value'] = pref.value('EnablePrefetcher').value()
        except:
            results['success'] = False

        return results

    def display_text(self, results, verbose):
        """Display results in console format"""
        print('------------------------ Prefetch ------------------------')
        if results['success']:
            if verbose > 0:
                print('Registry Key : %s' % self.KEY)
                print('')
                print('Prefetch status: %i - %s' % (results['value'], self.VALUES[results['value']]))
            else:
                print('Prefetch status: %s' % self.VALUES[results['value']])

            if verbose > 0:
                print("")
                for a in self.VALUES.keys():
                    print("%i: %s" % (a, self.VALUES[a]))
        else:
            print("No prefetch param: Boot and Application prefetch should be enabled")

