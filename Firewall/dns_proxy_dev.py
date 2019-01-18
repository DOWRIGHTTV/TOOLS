#!/usr/bin/python3

#from __future__ import print_function
#from scapy.all import *
import subprocess
from socket import AF_INET, SOCK_DGRAM, socket

import sniffer as sniff
import dnsresponse as DNR
import os

class WebFilter:
	def __init__(self):
		self.DEVNULL = open(os.devnull, 'wb')
		self.build_filter = "dst port 53"
		self.urldict = {}
		
		self.dictload()
		self.sniffer()
	
	def dictload(self):
		with open('Blacklist', 'r') as BL:
			while True:
				urL = BL.readline().strip().lower()
				if (not urL):
					break	
				urlP = urL.split('.')
				F1 = urlP[0]
				F2 = urlP[1]
				urLHex = '{}|{:02d}|{}'.format(F1, len(F2), F2) # len(F1), |{:02d}|
				self.urldict[urL] = [urLHex, 0]

	def sniffer(self):
	
#		sniff(iface="enp0s8", filter=self.build_filter, prn=self.custom_action, promisc=1)
        
		self.sn = sniff.Sniffer(iface='eth0', AK=self.url_check)
        
		
	def url_check(self, packet):
	    p = packet
		try:			
			reQ = p.qname						
			if ('www' not in reQ):
				reQ2 = 'www.{}'.format(reQ)
			
			if (reQ in self.urldict or reQ2 in self.urldict):
				urL = self.urldict[reQ][0]
				if (self.urldict[reQ][1] == 0):
					self.urldict[reQ][1] += 1
					subprocess.call(['sudo', 'iptables', '-I', 'FORWARD', '-m', 'string', '--hex-string', urL, '--algo', 'bm', '-j', 'DROP'])
					DNR.DNS_Response(packet)
					print('Pointing {} to Firewall'.format(reQ))
				else:
					self.urldict[reQ][1] += 1
					print(self.urldict[reQ][1])

					DNR.DNS_Response(packet)
					print('Pointing {} to Firewall. already blocked.'.format(reQ))
		except Exception as E:
			pass
		
		return
WebFilter()
