#!/usr/bin/python3

import socket
import sys
import os
import os.path
import subprocess

import time
import datetime
from multiprocessing.dummy import Pool as ThreadPool
import itertools

from netaddr import IPNetwork

ts = time.time()
dt = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
i = 0

##--------------------------------------------------------------------------------##
## Section X: Ping Sweep                                                          ##
##--------------------------------------------------------------------------------##
## Primary Ping Sweep Code ##
def Init():
	targetList = input('Name output file: ')
	if os.path.isfile (targetList):
		print('File already Exists. Please Try Again.')
		Init()
	else:
		iPRange(targetList)
def iPRange(targetList):	
	target_ip = input('Enter IP RANGE. ex. 192.168.1.0/24: ')
	iPRange2(target_ip, targetList)

def iPRange2(target_ip, targetList):
##section for calculating number of IPs##
	subnetstr = target_ip.strip()
	if subnetstr.endswith('/24'):
		total2 = 256
	elif subnetstr.endswith('/25'):
		total2 = 128
	elif subnetstr.endswith('/26'):
		total2 = 64
	elif subnetstr.endswith('/27'):
		total2 = 32
	elif subnetstr.endswith('/28'):
		total2 = 16
	elif subnetstr.endswith('/29'):
		total2 = 8
	elif subnetstr.endswith('/30'):
		total2 = 4
	elif subnetstr.endswith('/31'):
		total2 = 2
	else:
	    print('supports /24+ only')
	    iPRange(targetList)
	Netmask_Breakdown(total2, target_ip, targetList)
		
def tPools(total2, targetList):
	threadCounT = total2/3
	threadCount = int(threadCounT)
	print(('%s %s%s%s' % ('Using Optimal Threads', '[', threadCount, '].')))
	multiProc(total2, targetList, threadCount)
		
def Netmask_Breakdown(total2, target_ip, targetList):
	Q = 1
#	host_temP = open('host_temp1!@#!', 'a+')
	with open('host_temp1!@#!', 'a+') as host_temP:
		for subhostIP in IPNetwork(target_ip):
			if (Q == 1):
				Q = Q + 1
				pass
			else:		
				host_temP.write('%s \n' % (subhostIP))
	tPools(total2, targetList)

	
def multiProc(total2, targetList, threadCount):
	pooL = ThreadPool(threadCount)
	tarGetIP = []
	with open('host_temp1!@#!') as BANG:		
		total2 = total2 - 1
		for entrY in BANG:
			tarGetIP.append(entrY)
			pass
	SweepResults = pooL.map( PSweep, zip(tarGetIP, itertools.repeat(total2)))
	with open(targetList, 'w+') as blah2:
		for resIP, statuS in SweepResults:
			if (statuS == 0):
					blah2.write('%s \n' % (resIP))		
			else:
				pass
	pooL.close()
	pooL.join()
	PSFinal(targetList)
	
## loop for subnet masks
def PSweep(cB):
	global i
	tarGetIP = cB[0].strip()
	total2 = cB[1]
	DEVNULL = open(os.devnull, 'wb')
	res = subprocess.call(['ping', '-c', '1', str(tarGetIP)], stdout = DEVNULL)
	i = i + 1
	progress(i, total2)
	return tarGetIP, res
## Option to view results ##
def PSFinal(targetList):
	viewSResults = input("\nView results? Y or N: ")
	if (viewSResults == 'y'):
		with open(targetList) as F:	   
			F.seek(0)
			print('||The following HOSTS responded||')
			print("---------------------------------")
			for linE in F:
				if (linE == None):
					print('||No Hosts Responded :((||')
					os.remove(targetList)
				else:
					print((str(linE).strip()))		
	elif (viewSResults == 'n'):
		PSClose()
	else:
		print("Select Y or N.")
		PSweep2()
	PSClose()
##Exit program portion##
def PSClose():
	os.remove('host_temp1!@#!')
	print("--------------------------------------------------------")
	print('Exiting Ping Sweep v2 by JOE MAMA')
	print("--------------------------------------------------------")
	exit()
##---------------------------------------------------------------------------------##
##Section 4: Progress BAR MAIN                                                     ##
##---------------------------------------------------------------------------------##
def progress(count, total):
		bar_len = 42
		filled_len = int(round(bar_len * count / float(total)))
		percents = round(100.0 * count / float(total), 1)
		bar = '#' * filled_len + '=' * (bar_len - filled_len)
		space = '{message: <0}'.format(message='')
		time2 = time.ctime()
		sys.stdout.write('%s %s %s [%s] %s%s\r' % (time2, '||', space, bar, percents, '%'))
		sys.stdout.flush()
##---------------------------------------------------------------------------------##
## Section 7: Initialization                                                       ##
##---------------------------------------------------------------------------------##
if __name__ == '__main__':
	try: 
		Init()
	except Exception as E:
		print(E)
		try:
			os.remove('host_temp1!@#!')
		except Exception as Z:
			pass
	except KeyboardInterrupt:
		try:
			os.remove('host_temp1!@#!')
		except Exception as Z:
			pass
			print("\n--------------------------------------------------------")
