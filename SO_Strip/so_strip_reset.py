#!/usr/bin/python3

import os
import subprocess

class SOReset:
	def __init__(self):
		self.sO = '/etc/nsm/securityonion.conf'
		self.sE = ''
		self.snO = ''
		self.diS = '/etc/nsm/pulledpork/disablesid.conf'
		self.pP = '/etc/nsm/pulledpork/pulledpork.conf'
		self.fileS = [self.sO, self.diS, self.pP]  
		self.DEVNULL = open(os.devnull, 'wb')  
	
		self.SensorInfo()
		self.Reset()
		
	def SensorInfo(self):
		CompName = input('What is the name of Computer? eg. snort-box: ') 
		IntName = input('What is the name of the Sniffer Interface? eg. enp0s8: ')
		answeR = input(('%s-%s Selected. Confirm? [Y/n]: ' % (CompName, IntName)))
		if (answeR == 'y' or answeR == ''):		
			self.sE = '/etc/nsm/{}-{}/sensor.conf'.format(CompName, IntName)
			self.snO = '/etc/nsm/{}-{}/snort.conf'.format(CompName, IntName)
			if (os.path.isfile (self.sE) and os.path.isfile (self.snO)):
				self.fileS.append(self.sE)
				self.fileS.append(self.snO)
			else:
				print(('%s-%s not valid. Try Again.' % (self.CompName, self.IntName)))
				self.SensorInfo()
		elif (answeR == 'n'):
			self.SensorInfo()
		else:
			print('Invalid entry. Try again')
			self.SensorInfo()
			
	def Reset(self):
		for file in self.fileS:
			try:
				print('{}.bak'.format(file))
				subprocess.call(['sudo', 'cp', '{}.bak'.format(file), file])#, stdout = self.DEVNULL)
			except Exception as E:
					print('Error Restoring {} File.'.format(file))
		
	
	
	
	
	
	
	
	
	



