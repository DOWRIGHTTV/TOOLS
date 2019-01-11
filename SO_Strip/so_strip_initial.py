#!/usr/bin/python3


import fileinput
import os
import subprocess
import time

import server_VARS as sVARs



class InfoSet:
	def __init__(self):
		self.sO = '/etc/nsm/securityonion.conf'
#		self.sE = ''
#		self.snO = ''
		self.diS = '/etc/nsm/pulledpork/disablesid.conf'
		self.pP = '/etc/nsm/pulledpork/pulledpork.conf'
		self.diC = 'preDisabledCATs.txt'
		self.fileS = [self.sO, self.diS, self.pP]
		
		self.SensorInfo()
		self.CPUnLogInfo()
		self.servID()
		self.pubInspect()
		
	def SensorInfo(self):
		CompName = input('What is the name of Computer? eg. snort-box: ') 
		IntName = input('What is the name of the Sniffer Interface? eg. enp0s8: ')
		answeR = input(('%s-%s Selected. Confirm? [Y/n]: ' % (CompName, IntName)))
		if (answeR == 'y' or answeR == ''):		
			self.sE = '/etc/nsm/{}-{}/sensor.conf'.format(CompName, IntName)
			self.snO = '/etc/nsm/{}-{}/snort.conf'.format(CompName, IntName)
#			self.sE = '/etc/nsm/' + CompName + '-' + IntName + '/sensor.conf'
#			self.snO = '/etc/nsm/' + CompName + '-' + IntName + '/snort.conf'
			if (os.path.isfile (self.sE) and os.path.isfile (self.snO)):
				self.fileS.append(self.sE)
				self.fileS.append(self.snO)
			else:
				print(('%s-%s not valid. Try Again.' % (CompName, IntName)))
				self.SensorInfo()
		elif (answeR == 'n'):
			self.SensorInfo()
		else:
			print('Invalid entry. Try again')
			self.SensorInfo()
			
	def CPUnLogInfo(self):
		self.cpU = input('How many CPU cores do you have/ want to use for inspection?: ')
		self.logTime = input('How long do you want to store alert data? (days): ')
		answeR2 = input(('%s Snort Processes - %s days. Confirm? [Y/n]: ' % (self.cpU, self.logTime)))
		if (answeR2 != 'y' and answeR2 != '' and answeR2 != 'n'):
			print('Invalid entry. Try again')
			self.CPUnLogInfo()			
	
	def servID(self):
		self.answeR3 = input('Do you have any servers on your network? [y/N]: ')
		if (self.answeR3 != 'y' and self.answeR3 != '' and self.answeR3 != 'n'):
			print('Invalid entry. Try again')
			self.servID()
			
	def pubInspect(self):
		self.answeR4 = input('Are you inspecting outside of your firewall? [y/N]: ')
		if (self.answeR4 != 'y' and self.answeR4 != '' and self.answeR4 != 'n'):
			print('Invalid entry. Try again')
			self.pubInspect()

class Configurating:
	def __init__(self, iS):
		self.iS = iS	
		self.servList = ['DNS', 'SMTP', 'HTTP', 'SQL', 'TELNET', 'SSH', 'FTP', 'SIP']
		self.mList = ['ELASTICSEARCH', 'LOGSTASH', 'KIBANA', 'ELASTALERT', 'CURATOR', 'FREQ_SERVER', 'DOMAIN_STATS']
		self.mList2 = ['BRO', 'OSSEC_AGENT']
		self.caTs = []
		
		self.disELKBO()
		self.CnLSet()
		if (self.iS.answeR3 == 'n' or self.iS.answeR3 == ''):
			self.disServ()
		if (self.iS.answeR3 == 'y'):
			sVARs.edit(self.iS.snO)
		self.disCAT()
		if (self.iS.answeR4 == 'y'):
			self.pubInput()
		
## -- Disable All but NSM required modules -- ##
	def disELKBO(self):
		for modulE in self.mList:
			with fileinput.FileInput(self.iS.sO, inplace=True) as file:
				for line in file:
					print(line.replace(modulE + '_ENABLED="yes"', modulE + '_ENABLED="no"'), end='')
#					print(line.replace(('{}_ENABLED="yes"'.format(modulE))), ('{}_ENABLED="no"'.format(modulE)), end='')
		for modulE in self.mList2:
			with fileinput.FileInput(self.iS.sO, inplace=True) as file:
				for line in file:
					print(line.replace(modulE + '_ENABLED=yes', modulE + '_ENABLED=no'), end='')
#					print(line.replace(('{}_ENABLED=yes'.format(modulE))), ('{}_ENABLED=no'.format(modulE)), end='')
		print('ELK Stack, BRO, and OSSEC Modules disabled')

## -- CHANGE SNORT PROCESS COUNT AND ALERT LOG DAYS TO KEEP -- ##
	def CnLSet(self):
		with fileinput.FileInput(self.iS.sE, inplace=True) as file:
			for line in file:
				print(line.replace('IDS_LB_PROCS=1', 'IDS_LB_PROCS=' + self.iS.cpU), end='')
		with fileinput.FileInput(self.iS.sO, inplace=True) as file:
			for line in file:
					print(line.replace('DAYSTOKEEP=30', 'DAYSTOKEEP=' + self.iS.logTime), end='')

## -- CHANGE SERVERS TO NULL IP IF NO SERVERS PRESENT -- ##
## -- PREVENTION OF FALS POSITIVES OR NOISE --		   ##
	def disServ(self):
		for serveR in self.servList:
			with fileinput.FileInput(self.iS.snO, inplace=True) as file:
				for line in file:
					print(line.replace('ipvar ' + serveR + '_SERVERS $HOME_NET', 'ipvar ' + serveR + '_SERVERS [224.0.0.1]'), end='')
		return()

## -- DISABLING UNNEEDED ALERT CATEGORIES OR SERVER RELATED CATEGORIES -- ##
	def disCAT(self):
		print('Disabling unneeded rule categories. Edit disablesid.conf file to adjust as needed')
		if os.path.isfile (self.iS.diS):
			with open(self.iS.diC, 'r') as diCAT:
				for line in diCAT:
					self.caTs.append(line)
			with open(self.iS.diS, 'a') as diSID:
				for entry in self.caTs:
					diSID.write(entry)
			return()
		else:
			print("required file 'preDisabledCATs.txt' not found. Please DL.")
		
## -- OUTSIDE OF FIREWALL INSPECTION OPTIONS -- ##	
	def pubInput(self):
		homeNet = input('What is your public IP address subnet? : ')
		answeR = input(homeNet + ' selected. Confirm? [Y/n]: ')
		if (answeR == 'y' or answeR == ''):
			pass
		elif (answeR == 'n'):
			self.pubInput()
		else:
			print('Invalid entry. Try again')
			self.pubInput()
		with fileinput.FileInput(self.iS.snO, inplace=True) as file:
			for line in file:
				print(line.replace('ipvar HOME_NET [192.168.0.0/16,10.0.0.0/8,172.16.0.0/12]', 'ipvar HOME_NET [192.168.0.0/16,10.0.0.0/8,172.16.0.0/12,' + homeNet + ']'), end='')
		return()

## -- SCRIPT PREP, STOP SERVICES AND DISABLE ALL BUT NSM MODS -- ## 
class SystemTasks:
	def __init__(self, iS):
		self.iS = iS
		self.line = ('=========================================================')
		self.act = ('| %s Security Onion Services. This will take a bit |')
		self.DEVNULL = open(os.devnull, 'wb')
		
		self.Stop()
		
	def Stop(self):
## -- Stop ALL SecurityOnion services -- ##
#	filedata = filedata.replace((modulE + '_ENABLED="yes"', modulE + '_ENABLED="no"'), end='')		
		print(self.line)
		print((self.act % ('Stopping')))
		print(self.line)
		
		subprocess.call(['sudo', 'so-stop'], stdout = self.DEVNULL)
		
## -- Creating Backup Files -- ##
		print('Creating Backup files')
		try:
			for file in self.iS.fileS:
				subprocess.call(['cp', file, file + '.bak'], stdout = self.DEVNULL)
		# TOGGLE FOR INSTANT DELETION OF BACKUP FILES##
			subprocess.call(['rm', file + '.bak'], stdout = self.DEVNULL)
		except Exception as E:
			print('Error creating backup files. OH well...LOL')

	def Final(self):
		self.fL1()
		self.fL2()
		if (self.answeR == 'y' or self.answeR == ''):
			self.uFWset()
		else:
			print('Navigate to https://localhost/squert to start viewing alerts.')
			exit(3)
	
	def fL1(self):
		print(self.line)
		subprocess.call(['sudo', 'rule-update'])		
		print(self.line)
		print((self.act % ('Starting')))
		print(self.line)		
		subprocess.call(['sudo', 'so-start'], stdout = self.DEVNULL)

	def fL2(self):
		self.answeR = input('Will you be accessing from a different PC? [Y/n]: ')
		if (self.answeR != 'y' and self.answeR != '' and self.answeR != 'n'):
			print('Invalid entry. Try again')
			self.fL2()
			
	def uFWset(self):
		try:
			subprocess.call(['sudo', 'ufw', 'enable'], stdout = self.DEVNULL)
			subprocess.call(['sudo', 'ufw', 'allow', 'in', '443/tcp'], stdout = self.DEVNULL)
			subprocess.call(['sudo', 'ufw', 'allow', 'in', '22/tcp'], stdout = self.DEVNULL)	
			print('TCP/443 (HTTPS) and TCP/22 (SSH) allowed in firewall')
			exit(3)
		except Exception as E:
			print('Error configuring firewall. Manually enable/configure UFW')
			exit(3)

## PULLED PORK CLASS :D ##
## -- PULLED PORK SECTION -- ##
class PulledPork:
	def __init__(self, iS):
		self.iS = iS
		self.set_VARS()
		self.Main()
	
	def Main(self):	
		self.pP1()
		if (self.answeR1 == 'y' or self.answeR1 == ''):
			self.oC1()
			if (self.answeR2 == 'y' or self.answeR2 == ''):
				self.oC2()	   
				self.pP2()
			else:
				self.oC1()
		else:
			self.pP2()
	
	def pP1(self):
		self.answeR1 = input('Do you have an oinkcode? [Y/n]: ')
		if (self.answeR1 != 'y' and self.answeR1 != '' and self.answeR1 != 'n'):
			print('Invalid entry. Try again')
			self.pP1()
	def oC1(self):
		self.oinK = input('Enter Oink Code: ')
		self.answeR2 = input(('%s Entered. Confirm? [Y/n]: ' % (self.oinK)))
		if (self.answeR2 != 'y' and self.answeR2 != '' and self.answeR2 != 'n'):
			print('Invalid entry. Try again')
		
	def pP2(self):	
		print('Reconfiguring pulledpork.conf.')
		with fileinput.FileInput(self.iS.pP, inplace=True) as file:
			for line in file:
				print(line.replace('#' + self.COMR, self.COMR), end='')
		for entry in self.liSt:
			with fileinput.FileInput(self.iS.pP, inplace=True) as file:
				for line in file:
				 	print(line.replace(entry, '#' + entry), end='')
		with fileinput.FileInput(self.iS.pP, inplace=True) as file:
			for line in file:
				print(line.replace(self.ipbOLD, self.ipbNEW), end='')
		with fileinput.FileInput(self.iS.pP, inplace=True) as file:
			for line in file:
				print(line.replace(self.iprOLD, self.iprNEW), end='')
		with fileinput.FileInput(self.iS.pP, inplace=True) as file:
			for line in file:
				print(line.replace(self.ettOLD, self.ettNEW), end='')			
		open('/etc/nsm/rules/iplistsIPRVersion.dat', 'a+').close()
	

	def oC2(self):
		with fileinput.FileInput(self.iS.pP, inplace=True) as file:
			for line in file:
				print(line.replace('#' + self.IPB + 'open', self.IPB + '<' + self.oinK + '>'), end='')
				
	def set_VARS(self):
		self.n1 = 'sorule_path=/usr/local/lib/snort_dynamicrules/'
		self.n2 = 'snort_path=/usr/bin/snort'
		self.n3 = 'config_path=/etc/nsm/templates/snort/snort.conf'
		self.liSt = [self.n1, self.n2, self.n3]
		## -- COMMUNITY RULE OPTION -- ##
		self.COMR = 'rule_url=https://snort.org/downloads/community/|community-rules.tar.gz|Community'
		## -- File Path Corrections - Blaclist and Version -- ##
		self.ipbOLD = 'black_list=/usr/local/etc/snort/rules/iplists/default.blacklist'
		self.ipbNEW = 'black_list=/etc/nsm/rules/black_list.rules'
		self.iprOLD = 'IPRVersion=/usr/local/etc/snort/rules/iplists'
		self.iprNEW = 'IPRVersion=/etc/nsm/rules/iplistsIPRVersion.dat'
	## -- ET RULE URL CHANGE -- CHANGE THE NEW URL HERE WHEN UPDATED##
		self.ettOLD = 'rule_url=https://rules.emergingthreats.net/|emerging.rules.tar.gz|open'
		self.ettNEW = 'rule_url=https://rules.emergingthreats.net/open/snort-2.9.0/|emerging.rules.tar.gz|open'
		
		self.IPB = 'rule_url=http://talosintelligence.com/feeds/ip-filter.blf|IPBLACKLIST|'		

## -- END PULLED PORK SECTION -- ##
## END PULLED PORK CLASS ##

class Main:
	def __init__(self):
		iS = InfoSet()
		sT = SystemTasks(iS)
		cfG = Configurating(iS)
		PulledPork(iS)
		sT.Final()
			

