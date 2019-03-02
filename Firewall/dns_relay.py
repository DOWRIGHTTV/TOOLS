#!/usr/bin/python3

import os
import struct
import traceback
import time
import threading

from socket import *
from config import *
from interface_info import Interface


class DNSRelay:
    def __init__(self):
        Int = Interface()
        self.laddr = Int.IP(INIFACE)
        self.qaddr = Int.IP(WANIFACE)
        self.opendns1 = ['208.67.222.222', True]
        self.opendns2 = ['208.67.222.220', True]
        self.opendnsList = [self.opendns1, self.opendns2]
        self.lport = 53
               
    def Start(self):
        Reach = threading.Thread(target=self.Reachability)
        Reach.daemon = True
        threading.Thread(target=self.Main).start()
        Reach.start()
     
    
    def Reachability(self):
        DEVNULL = open(os.devnull, 'wb')
        while True:
            for server in self.opendnsList:
                reach = subprocess.call(['sudo', 'ping', '-c', '1', server[0]], stdout = DEVNULL)
                if (reach == 0):
                    server[1] = True
#                    print('{}:{}'.format(server[0], server[1]))                    
                else:
                    server[1] = False
#                    print('{}:{}'.format(server[0], server[1]))                    
            time.sleep(10)

    def Main(self):
        try:        
            self.sock = socket(AF_INET, SOCK_DGRAM)
            self.sock.bind((self.laddr, self.lport))
            # listen for UDP datagrams
            print('[+] Listening -> {}:{}'.format(self.laddr, self.lport))
            while True:
                self.data, self.addr = self.sock.recvfrom(1024)
                start = time.time()
                try:
                    self.parse_init_query(self.data)
                    
                    if (self.qtype == b'\x01'):
                        Relay = threading.Thread(target=self.RelayThread)
                        Relay.daemon = True
                        Relay.start()
                    else:
                        pass
                except Exception as E:
                    print(E)                    
        except Exception as E:
            print(E)
            
    def RelayThread(self):
        sock = socket(AF_INET, SOCK_DGRAM)
        time.sleep(.1)
        for server in self.opendnsList:
            if (server[1] == True):
                sock.sendto(self.data, (server[0], 53))
                print('Request Relayed')
                data, addr = sock.recvfrom(1024)
                print('Request Received')
                break
            else:
                pass
        self.sock.sendto(data, self.addr)
               
#        print('--------------------------')
#        print(self.data2)
#        end = time.time()
#        print(end - start)
#        print('--------------------------')       

    def parse_init_query(self, data):
        header = data[:12]
        self.payload = data[12:]
        tmp = struct.unpack(">6H", header)
        j = self.payload.index(0) + 1 + 4
        self.qtype = self.payload[j-3:j-2]
                

if __name__ == "__main__":
    try:
#        Int = Interface()
#        insideip = Int.WanIP()
#        wanip = Int.InsideIP()
        
        DNS = DNSRelay()
        DNS.Start()
    except KeyboardInterrupt:
        exit(3)

