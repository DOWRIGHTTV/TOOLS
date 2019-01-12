#!/usr/bin/python3

## ------------------------------------------- ##
## TOR NODE EXIT LIST FOUND AT				 ##
## https://check.torproject.org/exit-addresses ##
## ------------------------------------------- ##

import argparse
from sys import argv

import requests


parser = argparse.ArgumentParser(description = 'Converts TOR Exit Node list file to a standard ACL')
parser.add_argument('-f', '--file', help='tor exit node file input')
parser.add_argument('-o', '--out', help='output file name', required=True)
parser.add_argument('-s', '--standard', help='output a standard ACL', action='store_true')
parser.add_argument('-e', '--extended', help='output an extended ACL', action='store_true')
parser.add_argument('-l', '--log', help='add log statement to ACL', action='store_true')
parser.add_argument('-g', '--get', help='get tor list from URL', action='store_true')
	
args = parser.parse_args(argv[1:])

f = args.file
o = args.out
s = args.standard
e = args.extended

l = args.log
g = args.get

urL = 'https://check.torproject.org/exit-addresses'

def tor_GetList():
	ipGetList = []
	response = requests.get(urL)
	lisT = response.content.decode().split('\n')
	for entrieS in lisT:
		if ('ExitAddress' in entrieS):
				g1, IP, g2, g3 = entrieS.split(' ')
				ipGetList.append(IP)
	print(('grabbed from %s' % (urL)))
	tor_parseR(ipGetList)

def tor_parseR(ipGetList):
	if (not g):
		ipList = []
		if (f):
			print(('grabbed from %s' % (f)))
			with open(f, 'r') as tL:
				for line in tL:
					if ('ExitAddress' in line):
						g1, IP, g2, g3 = line.split(' ')
						ipList.append(IP)
		elif (not f):
			pass
	if (g):
		ipList = ipGetList
	if (s):
		cisco_standard(ipList)
	elif (e):
		cisco_extended(ipList)
	else:
		cisco_standard(ipList)
		
def cisco_standard(ipList):
	with open(o, 'w+') as tACL:
		if (l):
			tACL.write('ip access-list standard TOR_BLOCK_IN')	
			for IP in ipList:
				tACL.write('\ndeny host ' + IP + ' log')
			tACL.write('\npermit any')
		if (not l):
			tACL.write('ip access-list standard TOR_BLOCK_IN')	
			for IP in ipList:
				tACL.write('\ndeny host ' + IP)
			tACL.write('\npermit any')

def cisco_extended(ipList):
	print('This is the text version or a rock roll.')
	print('too tired to add this part right now.')

if __name__ == '__main__':
	try:
		if (g):
			tor_GetList()
		if (not g):
			tor_parseR('NULL')
	except Exception as E:
		print(E)

