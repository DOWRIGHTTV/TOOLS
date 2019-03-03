#!/usr/bin/python3

#from __future__ import print_function
#from scapy.all import *
#from socket import AF_INET, SOCK_DGRAM, socket

import os, subprocess
import time, threading

from interface_info import *
from dnx_dbconnector import SQLConnector as DBConnector
from subprocess import run
from dns_proxy_response import DNSResponse
from config import HOMEDIR, INIFACE
from dns_proxy_sniffer import Sniffer

class DNSProxy:
    def __init__(self):
        Int = Interface()
        self.insideip = Int.IP(INIFACE)
        self.homedir = HOMEDIR
        self.iface = INIFACE
        self.DEVNULL = open(os.devnull, 'wb')
        self.urldict = {}
        
    def Start(self):
        self.ProxyDB()
        self.Dictload()
        self.Proxy()
        
    def ProxyDB(self):
        ProxyDB = DBConnector()
        ProxyDB.Connect()
        ProxyDB.Cleaner()
        ProxyDB.Disconnect()
    
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
        hittime = int(time.time())
        try:
            request = packet.qname
            if ('www' not in request):
                request2 = 'www.{}'.format(request)            
            if (request in self.urldict or request2 in self.urldict):
                ProxyDB = DBConnector()
                ProxyDB.Connect()
                url = self.urldict[request][0]
                category = self.urldict[request][1]
                if (self.urldict[request][2] == 0):
                    if (self.urldict[request][1] == 'malicious'):
                        self.urldict[request][2] += 1
                        run('iptables -I MALICIOUS -m string --hex-string "{}" --algo bm -j DROP'.format(url), shell=True)
                    else:
                        self.urldict[request][2] += 1
                        run('iptables -I BLACKLIST -m string --hex-string "{}" --algo bm -j DROP'.format(url), shell=True)                    
#                    end = time.time()
#                    print(end - start)
                    DNS = DNSResponse(self.iface, self.insideip, packet)
                    threading.Thread(target=DNS.Response).start()
                    ProxyDB.Input(request, category, hittime)
                    print('Pointing {} to Firewall'.format(request))
                else:
                    self.urldict[request][2] += 1
                    DNS = DNSResponse(self.iface, self.insideip, packet)
                    threading.Thread(target=DNS.Response).start()
                    ProxyDB.Input(request, category, hittime)
                    print('Pointing {} to Firewall. already blocked.'.format(request))
                ProxyDB.Disconnect()
        except Exception as E:
            print(E)    
        
if __name__ == '__main__':
    DNSP = DNSProxy()
    DNSP.Start()
