#!/usr/bin/python3

## ------------------------------------------- ##
## TOR NODE EXIT LIST FOUND AT				   ##
## https://check.torproject.org/exit-addresses ##
## ------------------------------------------- ##

import argparse
from sys import argv

import requests


parser = argparse.ArgumentParser(description = 'Converts TOR Exit Node list file to a standard ACL')
parser.add_argument('-g', '--get', help='get tor list from URL', action='store_true')
parser.add_argument('-s', '--standard', help='output a standard ACL', action='store_true')
parser.add_argument('-e', '--extended', help='output an extended ACL', action='store_true')
parser.add_argument('-l', '--log', help='add log statement to ACL', action='store_true')
parser.add_argument('-f', '--file', help='tor exit node file input')
parser.add_argument('-o', '--out', help='output file name', required=True)
	
args = parser.parse_args(argv[1:])

f = args.file
o = args.out
s = args.standard
e = args.extended

l = args.log
g = args.get

urL = 'https://check.torproject.org/exit-addresses'

class Main:
	def __init__(self):
		Gat = Gathering()
		if (g):
			Gat.tor_GetList()
		elif (not g):
			if (f):
				Gat.tor_LocalList()
			else:
				print('local file required if not using -g/--get option')   
		Cisco_ACLs(Gat)
			 
## Collecting TOR Exit node, either from URL Above or Local File
class Gathering:
	def __init__(self):
		self.ipList = []
 
	## -- get request --
	def tor_GetList(self):
		response = requests.get(urL)
		lisT = response.content.decode().split('\n')
		for line in lisT:
			if ('ExitAddress' in line):
					g1, IP, g2, g3 = line.split(' ')
					self.ipList.append(IP)
		print(('grabbed from %s' % (urL)))
		
	## -- local file
	def tor_LocalList(self):
		with open(f, 'r') as tL:
			for line in tL:
				if ('ExitAddress' in line):
					g1, IP, g2, g3 = line.split(' ')
					self.ipList.append(IP)
			print(('grabbed from %s' % (f)))

class Cisco_ACLs:
	def __init__(self, Gat):
		self.Gat = Gat
		if (s):
			self.c_standard()
		elif (e):
			self.c_extended()
			
	def c_standard(self):
		with open(o, 'w+') as tACL:
			if (l):
				tACL.write('ip access-list standard TOR_BLOCK_IN')	
				for IP in self.Gat.ipList:
					tACL.write('\ndeny host ' + IP + ' log')
				tACL.write('\npermit any')
			elif (not l):
				tACL.write('ip access-list standard TOR_BLOCK_IN')	
				for IP in self.Gat.ipList:
					tACL.write('\ndeny host ' + IP)
				tACL.write('\npermit any')

	def c_extended(self):
		with open(o, 'w+') as tACL:
			if (l):
				tACL.write('ip access-list extended TOR_BLOCK_IN')
				for IP in self.Gat.ipList:
					tACL.write('\ndeny ip host {} any log'.format(IP))
				tACL.write('\npermit ip any any')
			elif (not l):
				tACL.write('ip access-list extended TOR_BLOCK_IN')	
				for IP in self.Gat.ipList:
					tACL.write('\ndeny ip host {} any'.format(IP))
				tACL.write('\npermit ip any any')


if __name__ == '__main__':
	try:
		Main()
	except Exception as E:
		print(E)

