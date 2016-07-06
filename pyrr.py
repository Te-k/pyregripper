#!/usr/bin/env python2
from Registry import *
from plugins.base import init_plugins
from ripper import Ripper
import argparse
import sys
import os
import inspect
import logging


class VAction(argparse.Action):
    """Handle verbose options within argparse"""
    def __call__(self, parser, args, values, option_string=None):
        if values==None:
            values='1'
        try:
            values=int(values)
        except ValueError:
            values=values.count('v')+1
        setattr(args, self.dest, values)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse windows registry for interesting data')
    parser.add_argument('PATH',  type=str, help='PATH to the registry file or the system dir')
    parser.add_argument('-p', '--plugin', type=str, help='Plugin to be used', required=False)
    parser.add_argument('-l', help='List plugins', action='store_true', required=False)
    parser.add_argument('-v', nargs='?', action=VAction, dest='verbose')
    parser.add_argument('-f', '--format', choices=['text', 'csv', 'json'], default='text')


    if len(sys.argv) == 2:
        if sys.argv[1] == '-l':
            r = Ripper()
            r.list_plugins()
            sys.exit(0)
        else:
            args, unknown = parser.parse_known_args()
    else:
        args, unknown = parser.parse_known_args()

    ripper = Ripper(args.verbose)

    if os.path.isfile(args.PATH):
        if args.plugin is not None:
            if args.plugin not in ripper.plugin_names():
                print("Bad plugin")
                sys.exit(1)
            else:
                ripper.launch_plugin(args.PATH, args.plugin, args.format, unknown)
        else:
            ripper.analyze_hive(args.PATH, args.format)
    elif os.path.isdir(args.PATH):
        # Check if it is a Windows repository
        ripper.analyze_windows_directory(args.PATH, args.format)
    else:
        print('Wait, wait, wait! I want a hive or a Windows directory here, OK?')
        sys.exit(1)


