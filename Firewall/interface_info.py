#!/usr/bin/python3

import subprocess
from config import INIFACE


class Interface:
    def IP(self, interface):
        output = subprocess.check_output('ifconfig {}'.format(interface), shell=True).decode()
        output = output.splitlines(8)
        for line in output:
            if('inet6' in line):
                pass
            elif('inet' in line):
                line = line.strip().split(' ')
                ip = line[1]
#                print(ip)
                return(ip)

    def MTU(self, interface):
        i = 0
        output = subprocess.check_output('ifconfig {}'.format(interface), shell=True).decode()
        output = output.splitlines(8)
        for line in output:
            if(i == 0):
                i += 1
                line = line.strip().split(' ')
                mtu = line[4]
#                print(mtu)
                return(mtu)

    def Netmask(self, interface):
        output = subprocess.check_output('ifconfig {}'.format(interface), shell=True).decode()
        output = output.splitlines(8)
        for line in output:
            if('inet6' in line):
                pass        
            elif('netmask' in line):
                line = line.strip().split(' ')
                netmask = line[4]
#                print(netmask)
                return(netmask)

    def Broadcast(self, interface):
        output = subprocess.check_output('ifconfig {}'.format(interface), shell=True).decode()
        output = output.splitlines(8)
        for line in output:
            if('inet6' in line):
                pass        
            elif('broadcast' in line):
                line = line.strip().split(' ')
                broadcast = line[7]
#                print(broadcast)
                return(broadcast)
                                
if __name__ == '__main__':
    Int = Interface()
    Int.IP(INIFACE)
    Int.MTU(INIFACE)
    Int.Netmask(INIFACE)
    Int.Broadcast(INIFACE)
    

