#!/usr/bin/python3

import os, time, subprocess
import threading, asyncio
import struct

from socket import *
from config import INIFACE, LOCALNET
from interface_ip import Interface
from dhcp_leases import DHCPLeases
from dhcp_response import DHCPResponse

class DHCPServer:
    def __init__(self):
        Int = Interface()
        self.insideip = Int.IP(INIFACE)
        
        self.Leases = DHCPLeases()

    def Start(self):
        print("DHCP server is starting...\n")
        
        #--Creating Lease Dictionary--#
        self.Leases.BuildRange()
        self.Leases.ReadLeases()
        
        #Loading Lease Expiration Timer--##
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(asyncio.gather(
            self.Leases.Timer, self.Leases.WritetoFile )
            
        except Exception as E:
            print('AsyncIO General Error')
            
#        threading.Thread(target=self.Leases.Timer).start()
#        threading.Thread(target=self.Leases.WritetoFile).start()
        
        #--Creating Sockets--##
        
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
        self.s.setsockopt(SOL_SOCKET, SO_BROADCAST,1)
        self.s.bind(('0.0.0.0', 67))
        print("[+] Listening on Port 67")
        while True:
            try:
                self.rdata, self.addr = self.s.recvfrom(1024)
                print(self.addr)
                addr, port = self.addr
                print('Received {}:{}'.format(addr, port))
#                print(self.rdata)
                mtype, xID, mac, ciaddr, chaddr, options = self.Parse(self.rdata) #, requestedip
                if mtype == 1: #b'\x01':
                    threading.Thread(target=self.Response, args=(2, xID, mac, ciaddr, chaddr, options,)).start()
                elif mtype == 3: #b'\x03':
                    threading.Thread(target=self.Response, args=(5, xID, mac, ciaddr, chaddr, options,)).start()
                elif mtype == 7: #b'\x07':
                    threading.Thread(target=self.Leases.Release, args=(ciaddr,)).start()
                
            except Exception as LOL:
                print(LOL)
                
    def Response(self, mtype, xID, mac, ciaddr, chaddr, options):
        Response = DHCPResponse(mtype, xID, mac, ciaddr, chaddr, options, self.Leases)#, requestedip)
        sdata = Response.Assemble()
        
        print('Responding with TYPE: {}'.format(mtype))
        if (mtype == 3 and ciaddr != '0.0.0.0'):
            print('Sent {}:{}'.format(ciaddr, 68))
            self.s.sendto(sdata, (ciaddr, 68))
        elif (mtype == 1 or mtype = 3):
            print('Sent {}:{}'.format('255.255.255.255', 68))
            self.s.sendto(sdata, ('255.255.255.255', 68))

        print('=' * 32)

    def Parse(self, data):
#        print(data)
        options = []
        b = 0
        vsend = 0
        for byte in data:
            b += 1
            currentbyte = data[b - 1]
            if (currentbyte == 60):
                optlen = data[b]
                vendorspec = data[b + 1:b + 1 + optlen]
                vsend = b + 1 + optlen
            elif (b > vsend):
                if (currentbyte == 55):
                    b -= 1
                    break  

        bptype  = data[0]
        hwtype = data[1]
        hwlen = data[2]
        xID = data[4:8]
        ciaddr = data[11:15]
        mac = data[28:28+6] # MAC ONLY
        chaddr = data[28:28+16]
        mcookie = data[236:240]
        dhcpm = data[240]
        mlen = data[241]
        mtype = data[242]
        
        
        mac = struct.unpack("!6c", mac)
        m = []
        for byte in mac:
            m.append(byte.hex())

        cia = struct.unpack("!4B", ciaddr)
        
        mac = '{}:{}:{}:{}:{}:{}'.format(m[0], m[1], m[2], m[3], m[4], m[5])
        ciaddr = '{}.{}.{}.{}'.format(cia[0], cia[1], cia[2], cia[3])
                    
        paramreq = data[b]
        paramlen = data[b + 1]
        paramitems = data[b + 2:b + 2 + paramlen]
        
        for byte in paramitems:
            options.append(byte)
        
        print('MTYPE: {}'.format(mtype))
#        print('xID: {}'.format(xID))
#        print('CHADDR: {}'.format(chaddr))
#        print('OPTIONS: {}'.format(options))
        return(mtype, xID, mac, ciaddr, chaddr, options)
        
if __name__ == '__main__':
    DHCPServer = DHCPServer()
    DHCPServer.Start()
