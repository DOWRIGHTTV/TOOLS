#!/usr/bin/python3

import so_strip_cfg as soC
import so_strip_reset as soR
import os

class Main_Start:
	def __init__(self):
		print('Security Onion Strip Utility')
		print('[1] Initial Setup')
		print('[2] Set Config Files to Default')
		self.Main()
		
	def Main(self):
		self.answeR = input('Select option: ')
		if (int(self.answeR) == 1):
			soC.Main()
		elif (int(self.answeR) == 2):
			soR.SOReset()
		else:
			print('Not a valid selection. Try again.')
			self.Main()
		
if __name__ == '__main__':
	try:
		priV = os.geteuid()
		if (priV == 0):
			print(' _______  _______    _______  _______  ________  ___   _______ ')  
			print('|       ||       |  |       ||       ||   _    ||   | |       |') 
			print('|  _____||   _   |  |  _____||_     _||  |_|  _||   | |    _  |')  
			print('| |_____ |  | |  |  | |_____   |   |  |      |_ |   | |   |_| |')  
			print('|_____  ||  |_|  |  |_____  |  |   |  |   __   ||   | |    ___|')
			print(' _____| ||       |   _____| |  |   |  |  |  |  ||   | |   |    ') 
			print('|_______||_______|  |_______|  |___|  |__|  |__||___| |___|    ')
			Main_Start()
		else:
			print('This Utility requires Root Priveledges. Exiting...')
			exit(1)
	except Exception as E:
		print(E)
	except KeyboardInterrupt:
		print('\n-----------------------------------------------------')
		print("User Interrupt. Exiting Some Random Thing")
		print('-----------------------------------------------------')
