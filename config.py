#!/usr/bin/env python

import subprocess

CONFIG = "/boot/config.txt"


class Pi:
    """ Basic information and state about the platform """
    def __init__(self):
        cpuinfo = self.get_cpuinfo()
        self.hardware = cpuinfo['hardware']
        self.revision = cpuinfo['revision']
        self.serial = cpuinfo['serial']
        self.revision = cpuinfo['revision']
        self.eth0_mac = self.get_mac_address('eth0')
        self.wlan0_mac = self.get_mac_address('wlan0')

    def get_cpuinfo(self):
        """ Uses 'cat /proc/cpuinfo' from the shell to obtain attributes of cpu 
            Attributes are returned as a dictionary.
            Multicore CPUs have repeated attributes and only the last values are returned
        """
        cpuinfo = {}
        proc = subprocess.Popen(['cat', '/proc/cpuinfo'], stdout=subprocess.PIPE)
        for line in proc.stdout.readlines():
            if ':' in line:
                left, right = line.split(':', 1)
                left = left.strip().lower()
                right = right.strip()
                cpuinfo[left] = right

        return cpuinfo

    def get_mac_address(self, iface):
        """ Uses 'ifconfig' to obtain the MAC address for interface (e.g. eth0 or wlan0)
            Returns a colon delimited string.
        """
        proc = subprocess.Popen(['ifconfig', iface], stdout=subprocess.PIPE)
        first_line = proc.stdout.readlines()[0]
        left, mac = first_line.split("HWaddr")
        mac = mac.strip()
        return mac


pi = Pi()
print "serial:", pi.serial
print "eth0:", pi.get_mac_address('eth0')
print "wlan0:", pi.get_mac_address('wlan0')

