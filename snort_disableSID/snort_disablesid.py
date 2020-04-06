#!/usr/bin/python3

import os
import re
import argparse
from sys import argv

import requests

parser = argparse.ArgumentParser(description = 'Searches downloaded SNORT rules for string match to help disabling groups of rules.')
parser.add_argument('-v', '--verbose', help='prints output to screen', action='store_true')
parser.add_argument('-o', '--out', help='output file name')
parser.add_argument('-f', '--file', help='snort rules file input', required=True)
parser.add_argument('-s', '--string', help='string to look for eg. SSH', required=True)

args = parser.parse_args(argv[1:])

IN_FILE = args.file
OUT_FILE = args.out

STRING = args.string
VERBOSE = args.verbose

reg_msg = re.compile(r'msg:"(.*?)"')
reg_sid = re.compile(r'sid:(.*?);')

def _parse_snort():
	disable_list = []
	with open(IN_FILE, 'r') as snort_rules:
		for rule in snort_rules:
			if(STRING.lower() not in rule.lower() or '#' in rule): continue

			disable_list.append(rule)

	if (not disable_list):
		print(f'no matches for {STRING}.')
	elif (OUT_FILE):
		with open(OUT_FILE, 'w+') as out_file:
			_output(disable_list, VERBOSE, out_file)
	elif (VERBOSE or not OUT_FILE):
		_output(disable_list, VERBOSE)

def _output(disable_list, v, out_file=None):
	if (disable_list and (VERBOSE or out_file is None)):
		print('-'*27 + '\n#' + ' '*9 + 'matches' + ' '*9 + '#\n' + '-'*27)

	for rule in disable_list:
		msg = re.findall(reg_msg, rule)[0]
		sid = re.findall(reg_sid, rule)[0]

		if (VERBOSE or out_file is None):
			print(f'1:{sid} # {msg}')

		if (out_file):
			out_file.write(f'1:{sid} # {msg}\n')
	else:
		if (VERBOSE or out_file is None):
			print('-'*27)

	if (out_file):
		print(f'matches written to {OUT_FILE}')

if __name__ == '__main__':
	try:
		if os.path.isfile(OUT_FILE):
			while True:
				proceed = input(f'{OUT_FILE} already exists and will be overridden. proceed? [Y/n]: ')
				if proceed.lower() in ['y', '']:
					break
				elif proceed.lower() == 'n':
					print('exiting...')
					os._exit(0)
				else:
					print('invalid entry. try again.')

		_parse_snort()
	except Exception as E:
		print(E)


