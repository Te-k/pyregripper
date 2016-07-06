#! /usr/bin/env python
from plugins.base import Plugin
from Registry import *

class PluginAutoruns(Plugin):
    name = "autoruns"
    htype = ["NTUSER", "SYSTEM"]
    description = "List software launched at runtime (only registry entries of course)"

    def run(self, registry, verbose, params={}):
        results = {'run':[], 'runonce':[]}
        try:
            runonce = registry.open('Software\Microsoft\Windows\CurrentVersion\RunOnce')
            if len(runonce.values()) > 0:
                for val in runonce.values():
                    results['runonce'].append(val.value())
        except:
            pass

        try:
            runonce = registry.open('Software\Microsoft\Windows\CurrentVersion\Run')
            if len(runonce.values()) > 0:
                for val in runonce.values():
                    results['run'].append(val.value())
        except:
            pass
        return results

    def display_text(self, results, verbose):
        print('------------------------ Autoruns ------------------------')
        print('\Software\Microsoft\Windows\CurrentVersion\RunOnce')
        if results['runonce'] == []:
            print('\tNo entry')
        else:
            for val in results['runonce']:
                print('\t%s' % val)

        print('')
        print('\Software\Microsoft\Windows\CurrentVersion\Run')
        if results['run'] == []:
            print('\tNo entry')
        else:
            for val in results['run']:
                print('\t%s' % val)

