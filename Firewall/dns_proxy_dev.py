#!/usr/bin/python3

#from __future__ import print_function
#from scapy.all import *
#from socket import AF_INET, SOCK_DGRAM, socket

import subprocess
import sniffer as sniff
import dnsresponse as DNR
import os
import time
from config import HOMEDIR, INIFACE

import argparse
from sys import argv
import multiprocessing


class DNSProxy:
    def __init__(self):
        self.homedir = HOMEDIR
        self.iface = INIFACE
        self.DEVNULL = open(os.devnull, 'wb')
        self.urldict = {}
        
        
    def Start(self):
        self.Dictload()
        self.Sniffer()
    
    def Dictload(self):
        with open('{}/domainlists/Malicious.domains'.format(self.homedir), 'r') as BL:
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

    def Sniffer(self):
        
        self.sn = sniff.Sniffer(self.iface, AK=self.url_check)
       
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
                        subprocess.call(['sudo', 'iptables', '-I', 'MALICIOUS', '-m', 'string', '--hex-string', urL, '--algo', 'bm', '-j', 'DROP'])
                    else:
                        self.urldict[reQ][2] += 1
                        subprocess.call(['sudo', 'iptables', '-I', 'BLACKLIST', '-m', 'string', '--hex-string', urL, '--algo', 'bm', '-j', 'DROP'])
#                    end = time.time()
#                    print(end - start)
                    DNS = DNR.DNS_Response(self.iface, packet)
                    multiprocessing.Process(target=DNS.Response).start()
#                    DNR.DNS_Response(self.iface, packet)
                    print('Pointing {} to Firewall'.format(reQ))
                else:
                    self.urldict[reQ][2] += 1
                    DNS = DNR.DNS_Response(self.iface, packet)
                    multiprocessing.Process(target=DNS.Response).start()
#                    DNR.DNS_Response(self.iface, packet)
                    print('Pointing {} to Firewall. already blocked.'.format(reQ))
        except Exception as E:
            pass     
        
if __name__ == '__main__':
    DNSP = DNSProxy()
    DNSP.Start()
