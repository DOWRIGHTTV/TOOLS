#!/usr/bin/python3

#from __future__ import print_function
from scapy.all import *
import subprocess
## Create a Packet Counter
counter = 0
build_filter = "dst port 53" #& src port 53"
## Define our Custom Action function

class CustomAction:
	def __init__(self):
		self.DEVNULL = open(os.devnull, 'wb')
		self.sniffer()

	def sniffer(self):
	
		sniff(iface="eth0", filter=build_filter, prn=self.custom_action)
		
	def custom_action(self, packet):
#	global counter
		Q = 0
		reQ = packet[0][4].qname.decode()
#		packet[0].show()
		reQ = reQ[:-1]
		with open('Blacklist', 'r') as BL:
			with open('/etc/hosts', 'a') as hF:
				for dN in BL:
					if reQ in dN:
						g1, g2 = dN.split(' ')
#						hF.write('224.1.0.1 {}'.format(dN))
#						subprocess.call(['iptables', '-A', 'INPUT', '-i', 'eth0', '-m', 'string', '--hex-string', '|05|4chan|03|com', '--algo', 'bm', '-j', 'DROP'])
#						try:
#							subprocess.call(['sudo', 'iptables', '-D', 'INPUT', '-m', 'string', '--hex-string', '"{}"'.format(g2.strip('\n')), '--algo', 'bm', '-j', 'DROP'])
#						except Exception as E:
#							print(E)
						g2b = g2.strip()
						print(g2b)
						subprocess.call(['sudo', 'iptables', '-A', 'INPUT', '-m', 'string', '--hex-string', '{}'.format(g2b), '--algo', 'bm', '-j', 'DROP'])
#						res = subprocess.call(['ping', '-c', '1', str(tarGetIP)], stdout = DEVNULL)  
						print('Blocking {}. hehehe'.format(reQ))
		
		
			
		
#		for shit in packet[0][4]:
#			fuck = shit.decode()
#			print(fuck)
 
## Setup sniff, filtering for IP traffi


#def sniffer():
#	sniff(iface="eth0", filter=build_filter, count=10000, prn=CustomAction)

CustomAction()
