#!/usr/bin/python3

import subprocess
from config import WANIFACE, INIFACE



class Interface:
    def __init__(self): 
        self.wan = WANIFACE
        self.inside = INIFACE
    
    def WanIP(self):
        i = 0
        output = subprocess.check_output('ifconfig {}'.format(self.wan), shell=True).decode()
        output = output.splitlines(8)
        for line in output:
            if('inet' in line and i == 0):
                i += 1
                line = line.strip().split(' ')
                self.wanip = line[1]
#                print(self.wanip)                
                return(self.wanip)
                
    def InsideIP(self):
        i = 0
        output = subprocess.check_output('ifconfig {}'.format(self.inside), shell=True).decode()
        output = output.splitlines(8)
        for line in output:
            if('inet' in line and i == 0):
                i += 1
                line = line.strip().split(' ')
                self.insideip = line[1]
#                print(self.insideip)
                return(self.insideip)
                
if __name__ == '__main__':
    Int = Interface()
    Int.WanIP()
    Int.InsideIP()

