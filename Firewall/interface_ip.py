#!/usr/bin/python3

import subprocess



class Interface:
    def IP(self, interface):
        i = 0
        output = subprocess.check_output('ifconfig {}'.format(interface), shell=True).decode()
        output = output.splitlines(8)
        for line in output:
            if('inet' in line and i == 0):
                i += 1
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

                
if __name__ == '__main__':
    Int = Interface()
    Int.WanIP()
    Int.InsideIP()

