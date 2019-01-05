#!/usr/bin/python


import re
sRL = 'dl.rules'
import argparse
from sys import argv

import requests


parser = argparse.ArgumentParser(description = 'Searches downloaded SNORT rules and process disable entries')
parser.add_argument('-f', '--file', help='snort rules file input', required=True)
parser.add_argument('-s', '--string', help='string to look for eg. SSH', required=True)
parser.add_argument('-o', '--out', help='output file name')
parser.add_argument('-v', '--verbose', help='prints output to screen', action='store_true')
	
args = parser.parse_args(argv[1:])

f = args.file
o = args.out

s = args.string
v = args.verbose

regmsG = r'msg:"(.*?)"'
regsiD = r'sid:(.*?);'

def Alert_parseR():
	re.compile(regmsG)
	re.compile(regsiD)
	
	sList = []

	with open(f, 'r') as rL:
		with open(o, 'w+') as outf:
			for alerT in rL:
				if(s in alerT):
					sList.append(alerT)
			for alerT in sList:			
				msG = re.findall(regmsG, alerT)[0]
				siD = re.findall(regsiD, alerT)[0]
				if (v or not o):
					print(('Adding 1:%s # %s' % (siD, msG)))
				if (o):
					outf.write(('1:%s # %s\n' % (siD, msG)))

			

if __name__ == '__main__':
	try:
		Alert_parseR()
	except Exception as E:
		print(E)


