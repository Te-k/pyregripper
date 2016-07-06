#! /usr/bin/env python
from plugins.base import Plugin
import argparse
from Registry import *

def print_service(service):
    """Print information about a service"""
    ERRORS = {0:"IGNORE", 1:"NORMAL", 2:"SEVERE", 3:"CRITICAL"}
    START = {0: 'BOOT (Loaded by the kernel)',
        1:'System (loaded y the I/O subsystem)',
        2:'Auto-load (loaded by Service Control Manager',
        3:'On-demand (Loaded by Service Control Manaer)',
        4:'Disabled'}
    TYPE = {1:'kernel Service Driver',
            2:'File System Driver',
            8:'File System Driver Service',
            4:'Set of arguments for an adapter',
            0x10:'Win32 program',
            0x20:'Win32 Service',
            0x110:'Win32 program that run a process by itself',
            0x120: 'Win32 program that share a process'
        }
    print('- %s:' % service.name())
    try:
        print('\tDisplayName= %s' % service.value('displayName').value())
    except Registry.RegistryValueNotFoundException:
        print("\tDisplayName= No value")
    try:
        print('\tDriver Package Id: %s' % service.value('DriverPackageId').value())
    except Registry.RegistryValueNotFoundException:
        pass
    try:
        print('\tError Control: %s' % ERRORS[service.value('ErrorControl').value()])
    except Registry.RegistryValueNotFoundException:
        pass
    try:
        print('\tGroup: %s' % service.value('Group').value())
    except Registry.RegistryValueNotFoundException:
        pass
    try:
        print('\tImage Path: %s' % service.value('ImagePath').value())
    except Registry.RegistryValueNotFoundException:
        pass
    try:
        print('\tObject Name: %s' % service.value('ObjectName').value())
    except Registry.RegistryValueNotFoundException:
        pass
    try:
        print('\tStart: %s' % START[service.value('Start').value()])
    except Registry.RegistryValueNotFoundException:
        pass
    try:
        print('\tType: %s' % TYPE[service.value('Type').value()])
    except Registry.RegistryValueNotFoundException:
        pass
    print('')

class PluginService(Plugin):
    name = "services"
    htype = ["SYSTEM"]
    description = "List windows services in SYSTEM hive"

    def run(self, registry, verbose, params={}):
        parser = argparse.ArgumentParser()
        parser.add_argument('-r', type=str)
        args = parser.parse_args(params)

        if args.r == None:
            print("------------------------------ Services --------------------------")
            currentset = self.find_current(registry)
            services = registry.open(currentset + '\Services')
            for service in services.subkeys():
                print_service(service)
        else:
            # Search for the subkey
            currentset = self.find_current(registry)
            services = registry.open(currentset + '\Services')
            for service in services.subkeys():
                if args.r.lower() in service.name().lower():
                    print_service(service)
