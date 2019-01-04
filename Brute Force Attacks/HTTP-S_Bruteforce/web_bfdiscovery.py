#!/usr/bin/python3

from requests import session
#import urllib2
from bs4 import BeautifulSoup as bS

def Disc(urL):
	Q = 0
	cVList = []
	with session() as c:	
		resultS = c.get(urL)
#		htmL = urllib2.urlopen(urL)
		if 'WWW-Authenticate' in resultS.headers:
			pass
		elif 'WWW-Authenticate' not in resultS.headers:
			soup = bS(resultS.text, 'html.parser')
			forM = soup.find('form')
			akVal = forM.get('action')				
			inpuT = soup.find_all('input')
			for credVal in inpuT:
				try:
					cVal = credVal.get('id')
					if 'err_msg' in cVal:
						pass
					elif (Q <= 1):
						cVList.append(cVal)
#						print(cVList)
						Q = Q + 1
				except Exception as OHGOSH:
					continue
#				else:
#					print('else')
#					continue
		return akVal, cVList	



