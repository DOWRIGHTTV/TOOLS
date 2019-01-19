#!/usr/bin/python3

#from __future__ import print_function
#from scapy.all import *
#from socket import AF_INET, SOCK_DGRAM, socket

import subprocess
import sniffer as sniff
import dnsresponse as DNR
import os

import argparse
from sys import argv

parser = argparse.ArgumentParser(description = 'DNS PROXY. GOGO.')
parser.add_argument('-i', '--iface', help='interface to listen on', required=True)
	
args = parser.parse_args(argv[1:])

iface = args.iface


class WebFilter:
    def __init__(self, iface):
        self.iface = iface
        self.DEVNULL = open(os.devnull, 'wb')
        self.build_filter = "dst port 53"
        self.urldict = {}
        
        self.dictload()
        self.sniffer()
    
    def dictload(self):
        with open('Blacklist', 'r') as BL:
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
        try:
            reQ = p.qname
            if ('www' not in reQ):
                reQ2 = 'www.{}'.format(reQ)
            
            if (reQ in self.urldict or reQ2 in self.urldict):
                urL = self.urldict[reQ][0]
                if (self.urldict[reQ][2] == 0):
                    self.urldict[reQ][2] += 1
                    subprocess.call(['sudo', 'iptables', '-I', 'FORWARD', '-m', 'string', '--hex-string', urL, '--algo', 'bm', '-j', 'DROP'])
                    DNR.DNS_Response(self.iface, packet)
                    print('Pointing {} to Firewall'.format(reQ))
                else:
                    self.urldict[reQ][2] += 1
#                    print(self.urldict[reQ][2])
                    DNR.DNS_Response(self.iface, packet)
                    print('Pointing {} to Firewall. already blocked.'.format(reQ))
        except Exception as E:
            pass
        
        return
WebFilter(iface)
