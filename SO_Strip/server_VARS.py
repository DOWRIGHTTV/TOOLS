#!/usr/bin/python3

import collections
import fileinput

## -- Defining Server Variables -- ##


def edit(snO):
	servList = ['DNS', 'SMTP', 'HTTP', 'SQL', 'TELNET', 'SSH', 'FTP', 'SIP']
 
	sList = collections.OrderedDict()
    # initialize the OrderedDict to hold empty lists so we can hold user inputs later
	for serv in servList:
		sList[serv] = ''
	print('1. DNS   5. TELNET')
	print('2. SMTP  6. SSH')
	print('3. HTTP  7. FTP')
	print('4. SQL   8. SIP')
	sList = collections.OrderedDict(sList)
	options = []
	while True:
		serV = input('What servers do you have. Type done to continue: ')
		try:		
			if (int(serV) in range(0,9)):
				options.append(serV)
		except ValueError as vE:
			if (serV == 'done'):
				break
			else:
				print('not a valid entry')
	for option in options:
		num = int(option)
		service = list(sList.keys())[num-1]
		new_ips = input("List " + service + " servers (seperated by comma)\n:")
		sList[service] = new_ips
	for serVS in sList:
		if (not sList[serVS]):
			with fileinput.FileInput(snO, inplace=True) as file:
				for line in file:
					print(line.replace('ipvar ' + serVS + '_SERVERS $HOME_NET', 'ipvar ' + serVS + '_SERVERS [224.0.0.1]'), end='')
		else:
			with fileinput.FileInput(snO, inplace=True) as file:
				for line in file:
					print(line.replace('ipvar ' + serVS + '_SERVERS $HOME_NET', 'ipvar ' + serVS + '_SERVERS [' + sList[serVS] + ']'), end='')
	return()


