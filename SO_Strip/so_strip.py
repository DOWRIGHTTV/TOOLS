#!/usr/bin/python3


import fileinput
import os
import subprocess
import time

import server_VARS as sVARs

sO = '/etc/nsm/securityonion.conf'
sE = ''
snO = ''
diS = '/etc/nsm/pulledpork/disablesid.conf'
pP = '/etc/nsm/pulledpork/pulledpork.conf'
diC = 'preDisabledCATs.txt'

fileS = [sO, diS, pP]


##ADD IN VARIABLES FOR COMPUTER NAME and INTERFACE NAME##

def nameS():
	global sE
	global snO
	CompName = input('What is the name of Computer? eg. snort-box: ') 
	IntName = input('What is the name of the Sniffer Interface? eg. enp0s8: ')
	answeR = input(('%s-%s Selected. Confirm?: [Y/n]' % (CompName, IntName)))
	if (answeR == 'y' or answeR == ''):		
		sE = '/etc/nsm/' + CompName + '-' + IntName + '/sensor.conf'
		snO = '/etc/nsm/' + CompName + '-' + IntName + '/snort.conf'
		if (os.path.isfile (sE) and os.path.isfile (snO)):
			fileS.append(sE)
			fileS.append(snO)
			Step1()
		else:
			print(('%s-%s not valid. Try Again.' % (CompName, IntName)))
			nameS()
	elif (answeR == 'n'):
		nameS()
	else:
		print('Invalid entry. Try again')
		nameS()
	
def Init():
	print('Security Onion Strip Utility')
	print('[1] Initial Setup')
	print('[2] Set Config Files to Default')
	Init2()

def Init2():
	answeR = input('Select option: ')
	if (int(answeR) == 1):
		nameS()
	elif (int(answeR) == 2):
		gotootheroptionspage() # LOL
	else:
		Init()

## -- SCRIPT PREP, STOP SERVICES AND DISABLE ALL BUT NSM MODS -- ## 
def Step1():
## -- Stop ALL SecurityOnion services -- ##
	mList = ['ELASTICSEARCH', 'LOGSTASH', 'KIBANA', 'ELASTALERT', 'CURATOR', 'FREQ_SERVER', 'DOMAIN_STATS']
	mList2 = ['BRO', 'OSSEC_AGENT']
#	filedata = filedata.replace((modulE + '_ENABLED="yes"', modulE + '_ENABLED="no"'), end='')
	DEVNULL = open(os.devnull, 'wb')
	print('=========================================================')
	print('| Stopping Security Onion Services. This will take a bit |')
	print('=========================================================')
	subprocess.call(['sudo', 'so-stop'], stdout = DEVNULL)
	print('Done.')
	
## -- Creating Backup Files -- ##
	print('Creating Backup files')
	try:
		for file in fileS:
			subprocess.call(['cp', file, file + '.bak'], stdout = DEVNULL)
		# TOGGLE FOR INSTANT DELETION OF BACKUP FILES##
#			subprocess.call(['rm', file + '.bak'], stdout = DEVNULL)
	except Exception as E:
		print('Error creating backup files. Check Computer and Monitor interface names.')
		nameS()

## -- Disable All but NSM required modules -- ##
	for modulE in mList:
		with fileinput.FileInput(sO, inplace=True) as file:
			for line in file:
				print(line.replace(modulE + '_ENABLED="yes"', modulE + '_ENABLED="no"'), end='')
	for modulE in mList2:
		with fileinput.FileInput(sO, inplace=True) as file:
			for line in file:
				print(line.replace(modulE + '_ENABLED=yes', modulE + '_ENABLED=no'), end='')
	print('ELK Stack, BRO, and OSSEC Modules disabled')			
	Step2()


## -- PRIMARY SETUP ITEMS AND SNORT VARIABLES -- ##
def Step2():
	cpU = input('How many CPU cores do you have/ want to use for inspection?:')
	logTime = input('How long do you want to store alert data? (days): ')
	answeR = input(('%s Snort Processes - %s days. Confirm? [Y/n]: ' % (cpU, logTime)))
	if (answeR == 'y' or answeR == ''):
		CPUnLOG(cpU, logTime)
		snort_init()
	elif (answeR == 'n'):
		Step2()
	else:
		print('Invalid entry. Try again')
		Step2()
## -- CHANGE SNORT PROCESS COUNT AND ALERT LOG DAYS TO KEEP -- ##
def CPUnLOG(cpU, logTime):
	with fileinput.FileInput(sE, inplace=True) as file:
		for line in file:
			print(line.replace('IDS_LB_PROCS=1', 'IDS_LB_PROCS=' + cpU), end='')
	with fileinput.FileInput(sO, inplace=True) as file:
		for line in file:
				print(line.replace('DAYSTOKEEP=30', 'DAYSTOKEEP=' + logTime), end='')
	return()
	
def snort_init():
#	print('We will now define Snorts IP Variables')
#	print('Answer Following Questions. Separate entries with commas. use CIDR for IPs.')
	answeR = input('Do you have any servers on your network? [Y/n]: ')
	if (answeR == 'y' or answeR == ''):
		sVARs.edit(snO)
		pubInspect()
		catDIS()
		pulledPork1()
		finaLize1()
	elif (answeR == 'n'):
		servDIS()
		pubInspect()
		catDIS()
		pulledPork1()
		finaLize1()
	else:
		print('Invalid entry. Try again')
		snort_init()


####
def snort_detailed():
	homeNET = input('Local IP Ranges: ')
####

## -- CHANGE SERVERS TO NULL IP IF NO SERVERS PRESENT -- ##
## -- PREVENTION OF FALS POSITIVES OR NOISE --		   ##
def servDIS():
	servList = ['DNS', 'SMTP', 'HTTP', 'SQL', 'TELNET', 'SSH', 'FTP', 'SIP']
	for serveR in servList:
		with fileinput.FileInput(snO, inplace=True) as file:
			for line in file:
				print(line.replace('ipvar ' + serveR + '_SERVERS $HOME_NET', 'ipvar ' + serveR + '_SERVERS [224.0.0.1]'), end='')
	return()

## -- DISABLING UNNEEDED ALERT CATEGORIES OR SERVER RELATED CATEGORIES -- ##
def catDIS():
	print('Disabling unneeded rule categories. Edit disablesid.conf file to adjust as needed')
	if os.path.isfile (diS):
		caTs = []
		with open(diC, 'r') as diCAT:
			for line in diCAT:
				caTs.append(line)
		with open(diS, 'a') as diSID:
			for entry in caTs:
				diSID.write(entry)
		return()
	else:
		print("required file 'preDisabledCATs.txt' not found. Please DL.")
		return()

## -- PULLED PORK SECTION -- ##					
def pulledPork1():
	answeR = input('Do you have an oinkcode? [Y/n]: ')
	if (answeR == 'y' or answeR == ''):
	   oinK = oinkCode()
	   oinkCode2(oinK)	   
	   pulledPork2()
	   return()
	elif (answeR == 'n'):
		pulledPork2()
		return()
	else:
		print('Invalid entry. Try again')
		pulledPork1()
		
def pulledPork2():
	## -- SO_RULE OPTIONS -- ##
	n1 = 'sorule_path=/usr/local/lib/snort_dynamicrules/'
	n2 = 'snort_path=/usr/bin/snort'
	n3 = 'config_path=/etc/nsm/templates/snort/snort.conf'
	liSt = [n1, n2, n3]
	## -- COMMUNITY RULE OPTION -- ##
	COMR = 'rule_url=https://snort.org/downloads/community/|community-rules.tar.gz|Community'
	## -- File Path Corrections - Blaclist and Version -- ##
	ipbOLD = 'black_list=/usr/local/etc/snort/rules/iplists/default.blacklist'
	ipbNEW = 'black_list=/etc/nsm/rules/black_list.rules'
	iprOLD = 'IPRVersion=/usr/local/etc/snort/rules/iplists'
	iprNEW = 'IPRVersion=/etc/nsm/rules/iplistsIPRVersion.dat'
	## -- ET RULE URL CHANGE -- CHANGE THE NEW URL HERE WHEN UPDATED##
	ettOLD = 'rule_url=https://rules.emergingthreats.net/|emerging.rules.tar.gz|open'
	ettNEW = 'rule_url=https://rules.emergingthreats.net/open/snort-2.9.0/|emerging.rules.tar.gz|open'
	
	print('Reconfiguring pulledpork.conf.')
	with fileinput.FileInput(pP, inplace=True) as file:
		for line in file:
			print(line.replace('#' + COMR, COMR), end='')
	for entry in liSt:
		with fileinput.FileInput(pP, inplace=True) as file:
			for line in file:
			 	print(line.replace(entry, '#' + entry), end='')
	with fileinput.FileInput(pP, inplace=True) as file:
		for line in file:
			print(line.replace(ipbOLD, ipbNEW), end='')
	with fileinput.FileInput(pP, inplace=True) as file:
		for line in file:
			print(line.replace(iprOLD, iprNEW), end='')
	with fileinput.FileInput(pP, inplace=True) as file:
		for line in file:
			print(line.replace(ettOLD, ettNEW), end='')
			
	open('/etc/nsm/rules/iplistsIPRVersion.dat', 'a+').close()
	return()
	
def oinkCode():
	oinK = input('Enter Oink Code: ')
	answeR = input(('%s Entered. Confirm? [Y/n]: ' % (oinK)))
	if (answeR == 'y' or answeR == ''):
	   return(oinK)	   
	elif (answeR == 'n'):
		oinkCode()
	else:
		print('Invalid entry. Try again')
		oinkCode()

def oinkCode2(oinK):
	IPB = 'rule_url=http://talosintelligence.com/feeds/ip-filter.blf|IPBLACKLIST|'
	with fileinput.FileInput(pP, inplace=True) as file:
		for line in file:
			print(line.replace('#' + IPB + 'open', IPB + '<' + oinK + '>'), end='')
	return()
## -- END PULLED PORK SECTION -- ##


## -- OUTSIDE OF FIREWALL INSPECTION OPTIONS -- ##	
def pubInspect():
	answeR = input('Are you inspecting outside of your firewall? [y/N]: ')
	if (answeR == 'n' or answeR == ''):
		return()
	elif (answeR == 'y'):
		pubInput()
	else:
		print('Invalid entry. Try again')
		pubInspect()

def pubInput():
	homeNet = input('What is your public IP address subnet? : ')
	answeR = input(homeNet + ' selected. Confirm? [Y/n]: ')
	if (answeR == 'y' or answeR == ''):
		pass
	elif (answeR == 'n'):
		pubInput()
	else:
		print('Invalid entry. Try again')
		pubInput()
	with fileinput.FileInput(snO, inplace=True) as file:
		for line in file:
			print(line.replace('ipvar HOME_NET [192.168.0.0/16,10.0.0.0/8,172.16.0.0/12]', 'ipvar HOME_NET [192.168.0.0/16,10.0.0.0/8,172.16.0.0/12,' + homeNet + ']'), end='')
	return()
##

## -- CONFIGURING AUTO CATEGORIZATION FOR ET IP BLACKLIST -- ##
## -- DEPRECATED FUNCTION WITHIN SECURITY ONION -- ##
def autoCAT():
	acL = ['ET CINS', 'ET DROP', 'ET COMPROMISED']
	with open('/etc/nsm/securityonion/autocat.conf', 'a') as acF:
		for entry in acL:
			acF.write('none||ANY||ANY||ANY||ANY||ANY||ANY||%%REGEXP%%' + entry + '||17\n')
	return()
	
def finaLize1():
	DEVNULL = open(os.devnull, 'wb')
#	print('Starting Security Onion Services. This will take a bit')
	subprocess.call(['sudo', 'rule-update'])	
	
	print('=========================================================')
	print('| Starting Security Onion Services. This will take a bit |')
	print('=========================================================')
	subprocess.call(['sudo', 'so-start'], stdout = DEVNULL)
	print('Navigate to https://localhost/squert to start viewing alerts.')
	exit(3)	
	
if __name__ == '__main__':
	try:
		priV = os.geteuid()
		if (priV == 0):
			Init()
		else:
			print('This Utility requires Root Priveledges. Extiting...')
			exit(1)
	except Exception as E:
		print(E)
	except KeyboardInterrupt:
		print('-----------------------------------------------------')
		print("\nUser Interrupt. Exiting FTP Brute Force Attack Module")
		print('-----------------------------------------------------')
