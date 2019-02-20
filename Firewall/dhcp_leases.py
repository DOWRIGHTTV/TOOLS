#!/usr/bin/python3

import os, time, subprocess
import threading, asyncio
import struct

from socket import *
from config import INIFACE, LOCALNET, MACS
from interface_info import Interface

class DHCPLeases:
    def __init__(self):
        self.leasetable = {}
        self.whitelist = {}
        ipoctet = LOCALNET.split('.')
        self.iprange = '{}.{}.{}'.format(ipoctet[0], ipoctet[1], ipoctet[2])

    #--Persistent lease operations--#
    async def WritetoFile(self):
    #Lease Table Backup / RUNs EVERY HOUR#
        while True:
#            await asyncio.sleep(60)
            await asyncio.sleep(60 * 60)
            print('Backing up DNX DHCP Leases')
            with open('dnx.leases', 'w+') as leases:
                for ip, value in self.leasetable.items():
                    if (value is not None):
                        leases.write('{} {} {}\n'.format(ip, value[0], value[1]))                 
                    
    def ReadLeases(self):
        try:
            with open('dnx.leases', 'r') as leases:
                while True:
                    urlHex = ''
                    line = leases.readline().strip().lower()
                    if (not line):
                        break
                    line = line.split(' ')
                    ip = line[0]
                    timestamp = line[1]
                    mac = line[2]
                    self.leasetable[line[0]] = [timestamp, mac]
        except Exception as E:
            print(E)
    ## -- End of Persistent lease operations -- ##

    ## -- Initializing lease database operations -- ##            
    def BuildRange(self):
    ## -- Building whitelist lease table -- ##
        i = 5
        for mac in MACS:
            if (i <= 15):
                hostip = '{}.{}'.format(self.iprange, i)
                self.whitelist[hostip] = mac
                i += 1
            else:
                pass
    
    ## -- Building standard lease table -- ##
        timestamp = int(time.time())
        threads = []
        for i in range(16,221):
            hostip = '{}.{}'.format(self.iprange, i)
            threads.append(threading.Thread(target=self.ICMPThread, args=(hostip, timestamp)))
        for t in threads:    
            t.start()
        for t in threads:
            t.join()
        
    def ICMPThread(self, hostip, timestamp):
        response = self.ICMPWorker(hostip)
#        print('{} : {}'.format(hostip, response))
        if (response == 0):
            self.leasetable[hostip] = [timestamp, None]
        else:         
            self.leasetable[hostip] = None
    
    def ICMPWorker(self, hostip):
        DEVNULL = open(os.devnull, 'wb')
        res = subprocess.call(['ping', '-c', '1', str(hostip)], stdout = DEVNULL)	
        return(res)

    ## -- Ending Initializing lease database operations -- ##
    
    ## -- Purging Lease table / Checked every 5 minutes -- ##        
    async def Timer(self):
        while True:     
#            await asyncio.sleep(45)
            await asyncio.sleep(5 * 60)
            print('Purging DNX Lease Table (if needed)')
            for ip, value in self.leasetable.items():
                if (value is None):
                    pass
                else:
                    timestamp = int(time.time())
                    time_elapsed = timestamp - int(value[0])
                    if (time_elapsed >= 86800):
                        self.leasetable[ip] = None
                    else:
                        pass

    def Release(self, ip, mac):
        try:
            if (self.leasetable[ip] != None):
                if (self.leasetable[ip][0] == mac):
                    print('Releasing {} : {} from table'.format(ip, mac))
                    self.leasetable[ip] = None
            else:
                pass
        except Exception as E:
            pass

    ## -- Handing out IP Addresses to response class -- ##               
    def Handout(self, mac):
        if (mac in MACS):
            for ip, value in self.whitelist.items():
                if (value == mac):
                    return ip
                else:
                    pass
                    
        else:
            while True:
                for ip, value in self.leasetable.items():
                    if (value is None):
                        pass
                    elif (value[1] == mac):
                        timestamp = int(time.time())
                        self.leasetable[ip] = [timestamp, mac]
                        return ip
                    else:
                        pass
                for ip, value in self.leasetable.items():
                    if (value is None):
                        timestamp = int(time.time())
                        self.leasetable[ip] = [timestamp, mac]
                        return ip
                    else:
                        pass
                else:
                    return None
