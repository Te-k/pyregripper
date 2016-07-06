#! /usr/bin/env python
from plugins.base import Plugin
from Registry import *


class PluginVolumeShadow(Plugin):
    name = "volumeshadow"
    htype = ["SYSTEM"]
    description = "Display information on the Volume Shadow Copy"

    def run(self, registry, verbose, params={}):
        START = {
                0: 'BOOT',
                1:'System',
                2:'Auto-load',
                3:'On-demand',
                4:'Disabled'
        }

        res = {}

        try:
            currentset = self.find_current(registry)
        except:
            return res
        try:
            vss_service = registry.open(currentset + '\Services\VSS')
            res['status'] =  START[vss_service.value('Start').value()]
        except Registry.RegistryKeyNotFoundException:
            return res

        res['subkeys'] = {}
        KEYS = [ 'FilesNotToBackup', 'FilesNotToSnapshot', 'KeysNotToRestore']

        for key in KEYS:
            regkey = registry.open(currentset + '\Control\BackupRestore\\' + key )
            res['subkeys'][key] = {'timestamp' : [regkey.timestamp().strftime('%Y%m%d %H:%M:%S')]}
            for val in regkey.values():
                val2 = filter(lambda a:a != '', val.value())
                res['subkeys'][key][val.name()] = val2
        return res

    def display_text(self, res, verbose):
        print('------------------------ Volume Shadow ------------------------')
        if res == {}:
            print("No VSS Service on this hive")
        else:
            print('Service status: %s\n' % res['status'])

            for k in res['subkeys'].keys():
                print(k)
                for subk in res['subkeys'][k].keys():
                    if len(res['subkeys'][k][subk]) == 1:
                        print('\t%s: %s' % (subk, res['subkeys'][k][subk][0]))
                    else:
                        print('\t%s: ' % subk)
                        for subkk in res['subkeys'][k][subk]:
                            print('\t\t-%s' % subkk)
                print('\n')

