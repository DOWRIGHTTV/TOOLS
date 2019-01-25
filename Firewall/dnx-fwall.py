#!/usr/bin/python3

import os
import subprocess
import initialcfg as CFG
import dns_proxy_dev as DNSProxy

class Main_Start:
    def __init__(self):
        print('Python Firewall')
        print('[1] Initial Setup')
        print('[2] Run Firewall')
        print('[3] Edit Firewall Options')
        print('[4] NGFW-X Setting ;)')
        self.Main()
        
    def Main(self):
        self.answeR = input('Select option: ')
        if (int(self.answeR) == 1):
            CFG.Main()
        elif (int(self.answeR) == 2):
            DNSProxy.Start()
        elif (int(self.answeR) == 3):
            exit(3)
        elif (int(self.answeR) == 4):
            exit(3)
        else:
            print('Not a valid selection. Try again.')
            self.Main()
        
if __name__ == '__main__':
    try:
        priV = os.geteuid()
        if (priV == 0):
            print(' ______   __    _  __   __    _______  _     _  _______  ___      ___     ')
            print('|      | |  |  | ||  |_|  |  |       || | _ | ||   _   ||   |    |   |    ')
            print('|  _    ||   |_| ||       |  |    ___|| || || ||  |_|  ||   |    |   |    ')
            print('| | |   ||       ||       |  |   |___ |       ||       ||   |    |   |    ')
            print('| |_|   ||  _    | |     |   |    ___||       ||       ||   |___ |   |___ ')
            print('|       || | |   ||   _   |  |   |    |   _   ||   _   ||       ||       |')
            print('|______| |_|  |__||__| |__|  |___|    |__| |__||__| |__||_______||_______|')
            Main_Start()
        else:
            print('DNX FWALL requires Root Priveledges. Exiting...')
            exit(1)
    except Exception as E:
        print(E)
    except KeyboardInterrupt:
        print('\n-----------------------------------------------------')
        print("User Interrupt. Exiting Some Random Thing")
        print('-----------------------------------------------------')
