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


class DNSProxy:
    def __init__(self, iface, homedir):
        self.homedir = homedir
        self.iface = iface
        self.DEVNULL = open(os.devnull, 'wb')
        self.urldict = {}
        
        self.dictload()
        self.sniffer()
    
    def dictload(self):
        with open('{}/domainlists/Malicious.domains'.format(self.homedir), 'r') as BL:
            while True:
                urlT = BL.readline().strip().lower()
                if (not urlT):
                    break
                urlT = urlT.split(' ')
                urlP = urlT[0].split('.')
                cat = urlT[1]
                F1 = urlP[0]
                F2 = urlP[1]
                try:
                    F3 = urlP[2]
                    if (F3):
                        urLHex = '{}|{:02d}|{}|{:02d}|{}'.format(F1, len(F2), F2, len(F3), F3)
                        self.urldict[urlT[0]] = [urLHex, cat, 0]
                except Exception:
                    urLHex = '{}|{:02d}|{}'.format(F1, len(F2), F2)
                    self.urldict[urlT[0]] = [urLHex, cat, 0]

    def sniffer(self):
        
        self.sn = sniff.Sniffer(self.iface, AK=self.url_check)
       
    def url_check(self, packet):
        p = packet
        start = time.time()
        try:
            reQ = p.qname
            if ('www' not in reQ):
                reQ2 = 'www.{}'.format(reQ)
            
            if (reQ in self.urldict or reQ2 in self.urldict):
                urL = self.urldict[reQ][0]
                if (self.urldict[reQ][2] == 0):
                    self.urldict[reQ][2] += 1
                    subprocess.call(['sudo', 'iptables', '-I', 'MALICIOUS', '-m', 'string', '--hex-string', urL, '--algo', 'bm', '-j', 'DROP'])
                    end = time.time()
                    print(end - start)
                    DNR.DNS_Response(self.iface, packet)
                    print('Pointing {} to Firewall'.format(reQ))
                else:
                    self.urldict[reQ][2] += 1
#                    print(self.urldict[reQ][2])
                    DNR.DNS_Response(self.iface, packet)
                    print('Pointing {} to Firewall. already blocked.'.format(reQ))
        except Exception as E:
            pass      
#       return
        
        
class Start:
    def __init__(self):
#        with open('config.py', 'r') as CFG:
            
#            for line in CFG:
#               if ('INIFACE=' in line):
#                    iface = line[9:].strip('\n"')
#            CFG.seek(0)
#            for line in CFG:
#                if ('HOMEDIR=' in line):
#                    homedir = line[9:].strip('\n"')
        DNSProxy(INIFACE, HOMEDIR)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'DNS PROXY. GOGO.')
    parser.add_argument('-i', '--iface', help='interface to listen on', required=True)
	
    args = parser.parse_args(argv[1:])

    iface = args.iface

    WebFilter(iface)
