#!/usr/bin/python3

import time
import random
import threading
import os
import subprocess

from netaddr import IPNetwork


class PingSweep:
    def __init__(self, iprange):
        self.upList = [] 
        self.ipList = []
        self.iprange = iprange
    
    def Start(self):
        self.Thread()
        self.Complete()
        
    def bob(self, th, ipa):
        result = self.worker(th, ipa)
        if (result == 0):
            self.upList.append(ipa)

    def worker(self, thread, target):
        DEVNULL = open(os.devnull, 'wb')
        res = subprocess.call(['ping', '-c', '1', str(target)], stdout = DEVNULL)	
        return(res)

    def Thread(self):
        th = 0
        for t in IPNetwork(self.iprange):
            if (th == 0):
                th +=1
            else:
                self.ipList.append(t)
                th +=1

        th2 = 1
        for ipa in self.ipList:
            if (th2 < th-2):
                th2 += 1
                threading.Thread(target=self.bob, args=(th, ipa)).start()
            else:
                pass
            
    def Complete(self):
        print('||FOLLOWING IPs ARE UP||')
        print('-' * 24)
        for ip in self.upList:
            print(ip)
        
     
def Main():
           
    iprange = input('IP Range to scan: ')    
    PS = PingSweep(iprange)
    PS.Start()


if __name__ == '__main__':
    Main()







    
