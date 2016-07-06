from Registry import *
from plugins.base import init_plugins
import os

class Ripper(object):
    def __init__(self, verbose=0):
        self.verbose = verbose
        self.plugins = init_plugins()

    def list_plugins(self):
        """list available plugins"""
        print("----------------------------- plugins ------------------------------")
        for pname in self.plugins:
            print("- %s" % pname )
            print("\t%s %s" % (self.plugins[pname].htype, self.plugins[pname].description))
            print("")

    def plugin_names(self):
        """Return list of plugin names"""
        return self.plugins.keys()

    def launch_plugin(self, hivefile, plugin, output_format="text", args=[]):
        """Launch a plugin on a hive file"""
        reg = Registry.Registry(hivefile)
        plug = self.plugins[plugin]()
        res = plug.run(reg, self.verbose, args)
        plug.display(res, output_format, self.verbose)

    def analyze_hive(self, hivefile, output_format="text", hive_type=None):
        """Analyze a hive"""
        reg = Registry.Registry(hivefile)
        print('Launching all analyze plugins on %s hive %s' % (reg.hive_type().name, hivefile))
        if hive_type is None:
            hive_type = reg.hive_type().name
        for plugin in self.plugins:
            if hive_type in self.plugins[plugin].htype:
                pobj = self.plugins[plugin]()
                res = pobj.run(reg, self.verbose)
                pobj.display(res, output_format, self.verbose)

    def analyze_windows_directory(self, path, output_format="text"):
        """Find all hives and analyze them"""
	if os.path.isdir(os.path.join(path, "Windows")):
            print("Windows directory found, looking for hives")
            hives = [
                ['SYSTEM', 'Windows/System32/config/SYSTEM'],
                ['SAM', 'Windows/System32/config/SAM'],
                ['SECURITY', 'Windows/System32/config/SECURITY'],
                ['SOFTWARE', 'Windows/System32/config/SOFTWARE']
            ]
            for hive in hives:
                if os.path.isfile(os.path.join(path, hive[1])):
                    print('=============================================================')
                    print('Found %s hive at %s' % (hive[0], hive[1]))
                    self.analyze_hive(
                            os.path.join(path, hive[1]),
                            output_format,
                            hive[0]
                    )
                    print('')

            for subfile in os.listdir(os.path.join(path, 'Users')):
                ddir = os.path.join(path, 'Users', subfile)
                if os.path.isdir(ddir):
                    if os.path.isfile(os.path.join(ddir, "NTUSER.DAT")):
                        hive_path = os.path.join(ddir, "NTUSER.DAT")
                        print('=============================================================')
                        print('Found %s hive at %s' % ("NTUSER", hive_path))
                        self.analyze_hive(hive_path, output_format, "NTUSER")
                    print('')

        else:
            print("It does not look like a Windows directory...")


