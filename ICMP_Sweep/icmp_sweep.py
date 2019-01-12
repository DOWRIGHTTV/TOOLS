#!/usr/bin/python3

import socket
import sys
import os
import os.path
import subprocess

import time
import datetime
from multiprocessing import Pool as ThreadPool
import itertools

import random

from netaddr import IPNetwork

ts = time.time()
dt = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

i = 0

class Main:
	def __init__(self):
		Gl = General()
		aS = Assembling(Gl)
		PoolCreate(aS.tarGetIP, aS.total, aS.threadCount, Gl.resultsList)
		Gl.Final()

class General:
	def __init__(self):
		self.OutFile()
		self.TargRange()

	def OutFile(self):
		self.resultsList = input('Name output file: ')
		if os.path.isfile (self.resultsList):
			print('File already Exists. Please Try Again.')
			self.OutFile()
			
	def TargRange(self):	
		self.targ_ipR = input('Enter IP RANGE. ex. 192.168.1.0/24: ')
		answeR = input('{} Selected. Confirm? [Y/n]: '.format(self.targ_ipR))
		if (answeR == 'y' or answeR == ''):
			return()
		else:
			self.TargRange()
		
	#end of scan#
	def Final(self):
		viewSResults = input('View results? [Y/n]: ')
		if (viewSResults == 'y' or viewSResults == ''):
			with open(self.resultsList) as F:	   
#				F.seek(0)
				print('||The following HOSTS responded||')
				print("---------------------------------")
				for linE in F:
					if (linE == None):
						print('||No Hosts Responded :((||')
						os.remove(self.resultsList)
					else:
						print((str(linE).strip()))		
		elif (viewSResults == 'n'):
			exit(3)
		else:
			print('Invalid Entry. Try again')
			self.Final()

class Assembling:
	def __init__(self, Gl):
		self.Gl = Gl
		self.tarGetIP = []
		self.Subnet_Calc()
		self.tPools_Calc()
		self.TargList_Assemble()
		
	##calculating thread pools##  
	def tPools_Calc(self):
		tC = self.total/3
		self.threadCount = int(tC)
		print(('Using Optimal Threads %s%s%s' % ('[', self.threadCount, '].')))	

	##calculating number of IPs##   
	def Subnet_Calc(self): 
		subnetstr = self.Gl.targ_ipR.strip()
		if (subnetstr.endswith('/24')):
			self.total = 256
		elif (subnetstr.endswith('/25')):
			self.total = 128
		elif (subnetstr.endswith('/26')):
			self.total = 64
		elif (subnetstr.endswith('/27')):
			self.total = 32
		elif (subnetstr.endswith('/28')):
			self.total = 16
		elif (subnetstr.endswith('/29')):
			self.total = 8
		elif (subnetstr.endswith('/30')):
			self.total = 4
		elif (subnetstr.endswith('/31')):
			self.total = 2
		else:
			print('supports /24+ only')
			exit(0)

	def TargList_Assemble(self):
		Q = 1
		for subhostIP in IPNetwork(self.Gl.targ_ipR):
			if (Q == 1):
				Q = Q + 1
				pass
			elif (Q >= int(self.total)):
				pass
			else:	
				self.tarGetIP.append(subhostIP)


def PoolCreate(tarGetIP, tT, tC, resultsList):
	pooL = ThreadPool(tC)
	print('Scanning IP Range...')
	SweepResults = pooL.map( PSweep, zip(tarGetIP, itertools.repeat(tT)))		
	with open(resultsList, 'w+') as rL:
		for resIP, statuS in SweepResults:
			if (statuS == 0):
				rL.write('%s \n' % (resIP))		
			else:
				pass
				
def PSweep(cB):
	global i
	DEVNULL = open(os.devnull, 'wb')
	tarGetIP, tT = cB
	print(tarGetIP)
	try:
		res = subprocess.call(['ping', '-c', '1', str(tarGetIP)], stdout = DEVNULL)	
		return tarGetIP, res
	except Exception as E:
		pass
			


if __name__ == '__main__':
	try: 
		Main()
	except Exception as E:
		print(E)
	except KeyboardInterrupt:
		print("\n--------------------------------------------------------")
