#!/usr/bin/python3


import collections
import re
import fileinput
import subprocess

from config import *


class FW_Options:
    def __init__(self):
        self.macreg = re.compile('(?:[0-9a-fA-F]:?){12}')
        self.validIP = re.compile('^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
        self.line = '---------------------------'
        self.cfg = 'config.py'
        self.set_interface_names()
        self.set_lan_subnet()
        self.set_mode()
        if (int(self.mode) == 1):
            self.set_macs()
        self.set_cats()
        self.ext_dns()
        
        self.apply_cfg()    
        
    def set_interface_names(self):
        self.waniface = input('What is your WAN interface name? ')
        self.iniface = input('What is your Inside interface name? ')
        confirm = input('WAN: {} - Inside: {} selected. Confirm? [Y/n]: '.format(self.waniface, self.iniface))
        if (confirm == '' or confirm == 'y'):
            pass
        elif (confirm == 'n'):
            self.set_interface_names()
        else:
            print('Invalid entry. Try again.')
            self.set_interface_names()

    def set_lan_subnet(self):
        confirm = input('Use default local subnet? (192.168.10.0/24) [Y/n]: ')
        if (confirm == '' or confirm == 'y'):
            self.localnetid = '192.168.10.0'
            self.localnetmask = '/24'
            self.localnet = '{}{}'.format(self.localnetid.strip(), self.localnetmask.strip())
        elif (confirm == 'n'):
            localsubnet = input('Specify local subnet/mask: ')
            localsubnet = localsubnet.split('/')
            self.localnetid = localsubnet[0]
            self.localnetmask = '/' + localsubnet[1]
            self.localnet = '{}{}'.format(self.localnetid, self.localnetmask)
            confirm = input('{} selected. Confirm? [Y/n]: '.format(self.localnet))
            if (confirm == '' or confirm == 'y'):
                pass
            elif (confirm == 'n'):
                self.set_lan_subnet()
            else:
                print('Invalid entry. Try again.')
                self.set_lan_subnet()

        else:
            print('Invalid entry. Try again.')
            self.set_lan_subnet()
    
    def set_mode(self):
        print(self.line)
        print('Is your home router in AP mode or NAT mode?')
        print('AP mode recommended (Can filter by IP Address).')
        self.mode = input('1. AP mode - 2. NAT mode. [1/2]: ')
        if (int(self.mode) == 1):
            pass
        elif (int(self.mode) == 2):
            pass
        else:
            print('Invalid entry. Try again.')
            self.set_mode()
        
    def set_macs(self):
        self.macL = []
        print(self.line)
        print('Enter MAC address of allowed computers.')
        print('Format > (aa:aa:aa:aa:aa:aa) - Type done to continue.')
        while True:
            macadd = input(': ')
            if (macadd.lower() == 'done'):
                M = 1
                print('------MAC Address white list------')
                for mac in self.macL:                    
                    print('{}. {}'.format(M, mac))
                    M += 1
                confirm = input('Confirm MAC Address list? [Y/n]: ')
                if (confirm == '' or confirm == 'y'):
                    break
                elif (confirm == 'n'):
                    self.set_macs()
                else:
                    print('Invalid entry. Try again.')
                    self.set_macs()
            elif self.macreg.match(macadd):
                self.macL.append(macadd)
            else:
                print('Please enter valid mac address')
    
    def set_cats(self):
        catList = ['VPN', 'ADULT', 'DRUGS', 'GUNS', 'SOCIALMEDIA', 'ADS', 'DYNDNS']
            
        self.catDict = collections.OrderedDict()
        # initialize the OrderedDict to hold empty lists so we can hold user inputs later
        for cat in catList:
            self.catDict[cat] = ''
        print(self.line)
        print('[1] VPN    [5] SOCIAL MEDIA')
        print('[2] ADULT  [6] ADS')
        print('[3] DRUGS  [7] DYNDNS')
        print('[4] GUNS')
        options = []
        print('What categories do you want to block. Type done to continue.')
        while True:
            catnum = input('Category number: ')
            try:        
                if (int(catnum) in range(0,8)):
                    options.append(catnum)
            except ValueError as vE:
                if (catnum == 'done'):
                    break
                else:
                    print('Not a valid entry. Try again.')
        print('------Category Black List------')
        for option in options:
            num = int(option)
            cat = list(self.catDict.keys())[num-1]
            self.catDict[cat] = 1
            print(cat)
        confirm = input('Confirm category black list? [Y/n]: ')
        if (confirm == '' or confirm == 'y'):
            pass
        elif (confirm == 'n'):
                self.set_cats()
        else:
            print('Invalid entry. Try again.')
            self.set_cats()
                
    def ext_dns(self):
        print(self.line)
        ext_dns = input('Block external DNS resolvers? |Recommended| [Y/n]: ')
        if (ext_dns == '' or ext_dns == 'y'):
            self.ext_dns = True
        elif (ext_dns == 'n'):
            self.ext_dns = False
        else:
            print('Invalid entry. Try again.')
            self.ext_dns()
        
    def apply_cfg(self):
            ## -------- INTERFACE NAMES -------- ##
        with fileinput.FileInput(self.cfg, inplace=True) as file:
            for line in file:
                print(line.replace('WANIFACE="eth0"', 'WANIFACE="{}"'.format(self.waniface)), end='')
        with fileinput.FileInput(self.cfg, inplace=True) as file:
            for line in file:
                print(line.replace('INIFACE="eth1"'.format(self.iniface), 'INIFACE="{}"'.format(self.iniface)), end='')
                
            ## -------- CATEGORY BLOCKS -------- ##
        for cat in self.catDict:
            if (self.catDict[cat]):
                with fileinput.FileInput(self.cfg, inplace=True) as file:
                    for line in file:
                        print(line.replace('{}=0'.format(cat), '{}=1'.format(cat)), end='')
                          
            ## -------- EXTERNAL DNS -------- ##
        if (self.ext_dns == True):
            with fileinput.FileInput(self.cfg, inplace=True) as file:
                for line in file:
                    print(line.replace('EXTERNALDNS=False', 'EXTERNALDNS=True'), end='')
        try:            
            if (self.localnetid != '192.168.10.0'):
                with fileinput.FileInput(self.cfg, inplace=True) as file:
                    for line in file:
                        print(line.replace('LOCALNET="192.168.10.0/24"', 'LOCALNET="{}"'.format(self.localnet)), end='')
        except Exception as E:
            pass 
            ## -------- MAC WHITELIST -------- ##
        if (int(self.mode) == 1):
            M = 1
            for mac in self.macL:
                print('MAC{}={}'.format(M, M) + ' MAC{}={}'.format(M,mac))                
                with fileinput.FileInput(self.cfg, inplace=True) as file:
                    for line in file:
                        print(line.replace('MAC{}="{}"'.format(M, M), 'MAC{}="{}"'.format(M,mac)), end='')
                    M += 1

class FW_IFaceCheck:
    def __init__(self, FWO):
        self.FWO = FWO    
        self.wan_ip_check()
    
    def wan_ip_check(self):
        i = 0
        output = subprocess.check_output('ifconfig {}'.format(self.FWO.waniface), shell=True).decode()
        output = output.splitlines(8)
        for line in output:
            if('inet' in line and i == 0):
                i += 1
                line = line.strip().split(' ')
                self.wanip = line[1]
                    
class FW_IPTables:
    def __init__(self, iF, FWO):
        self.iF = iF
        self.FWO = FWO
        self.cChains = ['MALICIOUS', 'WHITELIST', 'BLACKLIST']
        try:
            self.create_new_chains()
            self.main_forward_set()
            self.main_input_set()
            self.main_output_set()
            self.NAT()
        except Exception as E:
            print(E)
            
    def create_new_chains(self):
        for chain in self.cChains:
            subprocess.call(['sudo', 'iptables', '-N', chain])
            subprocess.call(['sudo', 'iptables', '-A', chain, '-j', 'RETURN'])
        
    def main_forward_set(self):
        subprocess.call(['sudo', 'iptables', '-P', 'FORWARD', 'DROP'])
        if (EXTERNALDNS == True):        
            subprocess.call(['sudo', 'iptables', '-A', 'FORWARD', '-p', 'udp', '--dport', '53', '-j', 'REJECT'])
            subprocess.call(['sudo', 'iptables', '-A', 'FORWARD', '-p', 'tcp', '--dport', '53', '-j', 'REJECT'])
        elif (EXTERNALDNS == False): 
            for chain in self.cChains:
                subprocess.call(['sudo', 'iptables', '-A', 'FORWARD', '-p', 'udp', '--sport', '53', '-j', chain])
            for chain in self.cChains:
                subprocess.call(['sudo', 'iptables', '-A', 'FORWARD', '-p', 'udp', '--dport', '53', '-j', chain])
 
        subprocess.call(['sudo', 'iptables', '-A', 'FORWARD', '-i', INIFACE, '-j', 'ACCEPT'])
        subprocess.call(['sudo', 'iptables', '-A', 'FORWARD', '-m', 'conntrack', '--ctstate', 'RELATED,ESTABLISHED', '-j', 'ACCEPT'])
        
    def main_input_set(self):
        subprocess.call(['sudo', 'iptables', '-P', 'INPUT', 'DROP'])
        for chain in self.cChains:
            subprocess.call(['sudo', 'iptables', '-A', 'INPUT', '-p', 'udp', '--dport', '53', '-j', chain])
        subprocess.call(['sudo', 'iptables', '-A', 'INPUT', '-i', INIFACE, '-p', 'icmp', '--icmp-type', 'any', '-j', 'ACCEPT'])
        subprocess.call(['sudo', 'iptables', '-A', 'INPUT', '-m', 'conntrack', '--ctstate', 'RELATED,ESTABLISHED', '-j', 'ACCEPT'])

        subprocess.call(['sudo', 'iptables', '-A', 'INPUT', '-i', INIFACE, '-p', 'udp', '--dport', '53', '-j', 'ACCEPT'])
        subprocess.call(['sudo', 'iptables', '-A', 'INPUT', '-i', INIFACE, '-p', 'tcp', '--dport', '443', '-j', 'ACCEPT'])
        
    def main_output_set(self):
        subprocess.call(['sudo', 'iptables', '-P', 'OUTPUT', 'DROP'])
        subprocess.call(['sudo', 'iptables', '-A', 'OUTPUT', '-d', '{}'.format(LOCALNET), '-j', 'ACCEPT'])
        subprocess.call(['sudo', 'iptables', '-A', 'OUTPUT', '-s', self.iF.wanip, '-j', 'MALICIOUS'])        
        subprocess.call(['sudo', 'iptables', '-A', 'OUTPUT', '-s', self.iF.wanip, '-j', 'ACCEPT'])
        #put entry for list location#
        
    def NAT(self):
        subprocess.call(['sudo', 'iptables', '-t', 'nat', '-A', 'POSTROUTING', '-o', WANIFACE, '-j', 'MASQUERADE'])

class Main:
    def __init__(sef):
        FWO = FW_Options()
        iF = FW_IFaceCheck(FWO)
        FW_IPTables(iF, FWO)

if __name__ == '__main__':
    FWConfigure()    
