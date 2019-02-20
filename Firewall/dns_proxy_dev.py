#!/usr/bin/python3

#from __future__ import print_function
#from scapy.all import *
#from socket import AF_INET, SOCK_DGRAM, socket

import subprocess
import os
import time
import argparse
import multiprocessing

from interface_info import *
from subprocess import run
from dns_proxy_response import DNSResponse
from config import HOMEDIR, INIFACE
from dns_proxy_sniffer import Sniffer
from sys import argv

class DNSProxy:
    def __init__(self):
        Int = Interface()
        self.insideip = Int.IP(INIFACE)
        self.homedir = HOMEDIR
        self.iface = INIFACE
        self.DEVNULL = open(os.devnull, 'wb')
        self.urldict = {}
        
    def Start(self):
        self.Dictload()
        self.Proxy()
    
    def Dictload(self):
        with open('{}/domainlists/Blocked.domains'.format(self.homedir), 'r') as BL:
            while True:
                urlHex = ''
                line = BL.readline().strip().lower()
                if (not line):
                    break
                line = line.split(' ')
                domain = line[0].split('.')
                cat = line[1]
                for part in domain:
                    if (len(urlHex) == 0):
                        urlHex += part
                    else:
                        urlHex += '|{:02d}|{}'.format(len(part), part)               
                self.urldict[line[0]] = [urlHex, cat, 0]

    def Proxy(self):
    
        Proxy = Sniffer(self.iface, action=self.url_check)
        Proxy.Start()            
       
    def url_check(self, packet):
        p = packet
#        start = time.time()
        try:
            reQ = p.qname
            if ('www' not in reQ):
                reQ2 = 'www.{}'.format(reQ)            
            if (reQ in self.urldict or reQ2 in self.urldict):
                urL = self.urldict[reQ][0]
                if (self.urldict[reQ][2] == 0):
                    if (self.urldict[reQ][1] == 'malicious'):
                        self.urldict[reQ][2] += 1
                        run('iptables -I MALICIOUS -m string --hex-string "{}" --algo bm -j DROP'.format(urL), shell=True)
                    else:
                        self.urldict[reQ][2] += 1
                        run('iptables -I BLACKLIST -m string --hex-string "{}" --algo bm -j DROP'.format(urL), shell=True)
#                    end = time.time()
#                    print(end - start)
                    DNS = DNSResponse(self.iface, packet)
                    multiprocessing.Process(target=DNS.Response).start()
#                    DNR.DNS_Response(self.iface, packet)
                    print('Pointing {} to Firewall'.format(reQ))
                else:
                    self.urldict[reQ][2] += 1
                    DNS = DNSResponse(self.iface, self.insideip, packet)
                    multiprocessing.Process(target=DNS.Response).start()
#                    DNR.DNS_Response(self.iface, packet)
                    print('Pointing {} to Firewall. already blocked.'.format(reQ))
        except Exception as E:
            pass     
        
if __name__ == '__main__':
    DNSP = DNSProxy()
    DNSP.Start()
