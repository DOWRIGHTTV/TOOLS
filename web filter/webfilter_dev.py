#!/usr/bin/python3

#from __future__ import print_function
from scapy.all import *
import subprocess
## Create a Packet Counter
counter = 0
build_filter = "dst port 53" #& src port 53"
## Define our Custom Action function

class WebFilter:
	def __init__(self):
		self.DEVNULL = open(os.devnull, 'wb')
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
#				print(self.urldict)
	def packet_hold(self):
	    
	    
	    tc qdisc add dev eth0 root netem delay 100ms			


	def sniffer(self):
	
		sniff(iface="eth0", filter=build_filter, prn=self.custom_action)
		
	def custom_action(self, packet):
		reQ = packet[0][4].qname.decode().lower()
		
#		packet[0].show()
		reQ = reQ[:-1]
		reQ2 = 'www.{}'.format(reQ)
		
		if (reQ in self.urldict or reQ2 in self.urldict):
			urL = self.urldict[reQ][0]
			if (self.urldict[reQ][1] == 0):
				self.urldict[reQ][1] += 1
#				print(self.urldict[reQ][1])
				print(self.urldict[reQ])
				subprocess.call(['sudo', 'iptables', '-A', 'INPUT', '-m', 'string', '--hex-string', urL, '--algo', 'bm', '-j', 'DROP'])				
#				self.urldict[reQ][1] = cnt + 1
				print('Blocking {}. hehehe'.format(reQ))
			else:
				self.urldict[reQ][1] += 1
				print(self.urldict[reQ][1])
				print('{} already blocked.'.format(reQ))
				pass
		

WebFilter()
