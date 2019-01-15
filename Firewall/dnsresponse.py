#!/usr/bin/python3


from contextlib import closing
from socket import *
from scapy.all import *
import sys
import struct
import time
import binascii
import subprocess
import array

#dmac = 'aa:aa:aa:aa:aa:aa'
#smac = '0c:9d:92:18:34:6F'
		# Ethernet II (DIX) Protocol Types
#ETH_P_IP = 0x0800		# Internet Protocol packet 



class DNS_Response:
	def __init__(self, packet):
		self.iF = 'eth0'
		self.ip = IPPacket(packet)
		
		self.s = socket.socket(AF_PACKET, SOCK_RAW)
		self.s.bind((self.iF, 0))
		
		self.response()

	def response(self):
		self.ip.assemble_eth_fields()
		self.ip.assemble_ipv4_fields()
		self.ip.assemble_udp()
		self.ip.assemble_dns_fields()
		self.ip.assemble_QueryR_fields()
		
		complete =  self.ip.raw1 + self.ip.raw2 + self.ip.raw3  + self.ip.raw4 + self.ip.raw5
		self.s.send(complete)



class IPPacket:
	def __init__(self, packet):
		self.packet = packet
		self.split_packet()
		self.create_ipv4_fields_list()
		self.ipv4H = self.assemble_ipv4_fields()
		self.ip_chk = self.cksum(self.ipv4H)
		self.create_udp_fields()
		self.create_dns_fields()
		self.create_QueryR_fields()

	
	def split_packet(self):
		self.url = self.packet['DNS Question Record'].qname.decode().lower()
		self.url = self.url[:-1]
		self.smac = self.packet['Ethernet'].dst
		self.src = self.packet['IP'].dst
		self.sport = 53
		self.dmac = self.packet['Ethernet'].src
		self.dstip = self.packet['IP'].src
		self.dport = self.packet['UDP'].sport
		self.dst = (self.dstip,int(self.dport))
		self.dnsID = self.packet['DNS'].id
		
		# Ethernet II (DIX) Protocol Types
		self.l2pro = 0x0800		# Internet Protocol packet
		
	def cksum(self, s):
		if len(s) & 1:
			s = s + '\0'
		words = array.array('h', s)
		sum = 0
		for word in words:
			sum = sum + (word & 0xffff)
		hi = sum >> 16
		lo = sum & 0xffff
		sum = hi + lo
		sum = sum + (sum >> 16)
		return (~sum) & 0xffff
		
## -- L2 - Ethernet Section ---- ##
	def assemble_eth_fields(self):
# ---- Assemble All Fields Of Ether Packet ---- #
		self.raw1 = struct.pack('!6s6sH' ,
		binascii.unhexlify(self.dmac.replace(":","")),
		binascii.unhexlify(self.smac.replace(":","")),
		self.l2pro)
#		return(self.raw1)

## -- L3 - IP Section ---- ##		
	def create_ipv4_fields_list(self):
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
		self.ip_chk = 0						 # ---- [ Check Sum ]		
		self.ip_saddr = inet_aton(self.src)	 # ---- [ Source Address ]		
		self.ip_daddr = inet_aton(self.dstip)	 # ---- [ Destination Address ]
		return
	
	def assemble_ipv4_fields(self):
		self.raw2 = struct.pack('!BBHHHBBH4s4s' , 
		self.ip_ver,		# IP Version 
		self.ip_dfc,		# Differentiate Service Field
		self.ip_tol,		# Total Length
		self.ip_idf,		# Identification
		self.ip_flg,		# Flags
		self.ip_ttl,		# Time to leave
		self.ip_proto,		# protocol
		self.ip_chk,		# Checksum
		self.ip_saddr,		# Source IP 
		self.ip_daddr		# Destination IP
		)
		return(self.raw2)

## -- L4 - UDP Section ---- ##			
	def create_udp_fields(self):			
		self.udp_sport = 53  # ---- [ Source Port]		
		self.udp_dport = self.sport	# ---- [ Destination Port ]		
		self.udp_len = 26		# ---- [ Total Length ]		
		self.udp_chk = 0		# ---- [ Check Sum ]
		
	def assemble_udp(self):
		self.raw3 = struct.pack('!HHHH' ,
		self.udp_sport,		 # IP Version 
		self.udp_dport,		 # Differentiate Service Field
		self.udp_len,		 # Total Length
		self.udp_chk		 # Identification
		)
	def create_dns_fields(self):	
		self.id		= self.dnsID
		self.qr		= 1
		self.opcode	= 0
		self.aa		= 0
		self.tc		= 0
		self.rd		= 1
		self.ra		= 1
		self.z		 = 0
		self.ad		= 0
		self.cd		= 0
		self.rcode	 = 0
		self.qdcount   = 1
		self.ancount   = 1
		self.nscount   = 0
		self.arcount   = 0
		
	def assemble_dns_fields(self):
		self.p1 = (self.qr << 0) | (self.opcode << 1) | (self.aa << 2) | (self.tc << 3) | (self.rd << 7)
		self.p2 = (self.ra << 0) | (self.z << 4) | (self.ad << 5) | (self.cd << 6) | (self.rcode << 7)
		  
		self.raw4 = struct.pack('!H2B4H' ,
		self.id,
		self.p1,
		self.p2,
		self.qdcount,
		self.ancount,
		self.nscount,
		self.arcount
		)
		
	def create_QueryR_fields(self):
	 ###[ DNS Question Record ]###
		self.qname	 = self.url
		self.qtype	 = 251
		self.qclass	= 1

	 ###[ DNS Resource Record ]###
		self.rrname	= self.url
		self.type	  = 251
		self.rclass	= 1
		self.ttl	   = 146
		self.rdlen	 = 4
		self.rdata	 = inet_aton('192.168.10.1')
		self.ns		= None
		self.ar		= None
		
	def assemble_QueryR_fields(self):
	 ###[ DNS Question Record ]###
		split_url = self.url.split(".")
		self.urlpack = b''
		for part in split_url: # iterate (2) for madd and org
			self.urlpack += struct.pack("B", len(part))
			for char in part:
				self.urlpack += struct.pack("B", ord(char))
#		print(self.urlpack)          
		self.raw5 = self.urlpack + struct.pack('!2H' ,
		self.qtype,
		self.qclass
		)
		self.raw5 = self.urlpack + struct.pack('!2HLH4s' , 
	 ###[ DNS Resource Record ]###
		self.type,
		self.rclass,
		self.ttl,
		self.rdlen,
		self.rdata
		)
		
		#self.ns,
		#self.ar
		#)
		                
#			for byte in bytes(part, 'utf8'):
#				print(byte)
#				self.urlpack += struct.pack("c", byte)    
		
		
		
		
