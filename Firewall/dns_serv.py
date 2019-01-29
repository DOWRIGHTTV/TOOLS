#!/usr/bin/python3

import os
from socket import *
import struct
import traceback
import time
import threading



class DNSServer:
    def __init__(self):
        self.laddr = '192.168.83.3'
        self.qaddr = '192.168.2.78'
        self.lport = 53
        
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind((self.laddr, self.lport))

        self.sock2 = socket(AF_INET, SOCK_DGRAM)

    def Start(self):
        # listen for UDP datagrams
        print('[+] Listening -> {}:{}'.format(self.laddr, self.lport)) 
        while True:
            # receive and parse query
            self.data, self.addr = self.sock.recvfrom(1024)
            start = time.time()
            try:
                self.parse_init_query(self.data)
                if (self.qtype == b'\x01'):
                    print('Wait, then relay')
                    threading.Thread(target=self.RandR).start()
                else:
                    pass
            except Exception as E:
                pass   
    def RandR(self):
        time.sleep(.1)
        self.sock2.sendto(self.data, ('208.67.222.222', 53))
        print('Request Relayed')
        self.data2, self.addr2 = self.sock2.recvfrom(1024)
        print('Request recieved')
        self.sock.sendto(self.data2, self.addr)
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
        DNS = DNSServer()
        DNS.Start()
    except KeyboardInterrupt:
        exit(3)

