#!/usr/bin/python3

import os, time, subprocess
import threading, asyncio
import struct


from socket import *
from collections import OrderedDict 
from config import INIFACE, LOCALNET
from interface_info import Interface
from dhcp_leases import DHCPLeases
from dhcp_response import DHCPResponse

class DHCPServer:
    def __init__(self):
        self.Leases = DHCPLeases()
        self.ongoing = {}

    def Start(self):
        print("DHCP server is starting...")
        
        # -- Creating Lease Dictionary -- #
        self.Leases.BuildRange()
        self.Leases.ReadLeases()
        self.interfaceinfo = self.InterfaceInfo()

        threading.Thread(target=self.Server).start()
        threading.Thread(target=self.Timers).start()

    def Timers(self):
        ## -- Loading Lease Expiration Timer -- ##
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(asyncio.gather(self.Leases.Timer(), self.Leases.WritetoFile()))
        except Exception as E:
            print('AsyncIO General Error : {}'.format(E))
        
    def Server(self):
        ## -- Creating Sockets -- ##        
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
        self.s.setsockopt(SOL_SOCKET, SO_BROADCAST,1)
        self.s.setsockopt(SOL_SOCKET, SO_BINDTODEVICE, str(INIFACE + '\0').encode('utf-8'))
        self.s.bind(('0.0.0.0', 67))
        print("[+] Listening on Port 67")
        while True:
            try:
                Parse = DHCPParser(self.interfaceinfo)
                self.rdata, self.addr = self.s.recvfrom(1024)
                addr, port = self.addr
                print('Received from {}:{}'.format(addr, port))
                mtype, xID, mac, ciaddr, chaddr, options = Parse.Data(self.rdata)
                options = Parse.Options(options)
                threading.Thread(target=self.Response, args=(mtype, xID, mac, ciaddr, chaddr, options)).start()
            except Exception as E:
                print(E)
                
    def Response(self, mtype, xID, mac, ciaddr, chaddr, options):
        if (mac in self.ongoing and self.ongoing[mac] != xID):
            #options = {}
            options[53] = [1, 6]
            self.SendResponse(xID, mac, ciaddr, chaddr, options)
        elif mtype == 1: # b'\x01'
            options[53] = [1, 2]
            self.SendResponse(xID, mac, ciaddr, chaddr, options)
        elif mtype == 3: # b'\x03'
            options[53] = [1, 5]
            self.SendResponse(xID, mac, ciaddr, chaddr, options)
        elif mtype == 7: # b'\x07'
            self.Leases.Release(ciaddr, mac)
                    
    def SendResponse(self, xID, mac, ciaddr, chaddr, options):
        mtype = options[53][1]
        ## -- Set ongiong request flag, NAK duplicates -- ##  
        if (mtype not in {6}):
            self.ongoing[mac] = xID
            threading.Thread(target=self.OngoingTimer, args=(mac,)).start()
            
        Response = DHCPResponse(xID, mac, ciaddr, chaddr, options, self.Leases)
        sdata = Response.Assemble()   
        if (mtype in {2,5,6}):
            if (ciaddr != '0.0.0.0'):
                print('Sent TYPE: {} to {}:{}'.format(mtype, ciaddr, 68))
                self.s.sendto(sdata, (ciaddr, 68))
            else:
                print('Sent TYPE: {} to {}:{}'.format(mtype, '255.255.255.255', 68))
                self.s.sendto(sdata, ('255.255.255.255', 68))
            
        ## -- Remove ongiong request flag, NAK duplicates -- ##
        if (mac in self.ongoing and mtype in {5}):
            del self.ongoing[mac]
        print('=' * 32)
        
    def OngoingTimer(self, mac):
        time.sleep(6)
        if (mac in self.ongoing):
            del self.ongoing[mac]

    def InterfaceInfo(self):
        Int = Interface()
        insideip = Int.IP(INIFACE)
        netmask = Int.Netmask(INIFACE)
        broadcast = Int.Broadcast(INIFACE)
        mtu = Int.MTU(INIFACE) 
        
        return(insideip, netmask, broadcast, mtu)


class DHCPParser:
    def __init__(self, interfaceinfo):
        self.insideip = interfaceinfo[0]
        self.netmask = interfaceinfo[1]
        self.broadcast = interfaceinfo[2]
        self.mtu = interfaceinfo[3]
        
        self.optset = {1, 3, 6, 26, 28, 51, 58, 59} # 54,
        self.optnums = [1, 3, 6, 26, 28, 51, 58, 59] # 54,
        self.optnames = ['subnetmask', 'router', 'dnsserver', 'mtu', 'broadcast',
                    'leasetime', 'renewtime', 'rebindtime']
                    #'dhservident', 'mtypeopt']
                
        self.subnetmask = [4, inet_aton(self.netmask)]         # OPT 1
#        self.router = [4, inet_aton('192.168.5.1')]           # OPT 3        
        self.router = [4, inet_aton(self.insideip)]            # OPT 3
#        self.dnsserver = [4, inet_aton('192.168.5.1')]        # OPT 6  
        self.dnsserver = [4, inet_aton(self.insideip)]         # OPT 6
        self.mtu = [2, int(self.mtu)]                          # OPT 26
        self.broadcast = [4, inet_aton(self.broadcast)]        # OPT 28
        self.leasetime = [4, 86400]                            # OPT 51
#        self.dhservident = [4, inet_aton('192.168.5.1')]      # OPT 54
        self.dhservident = [4, inet_aton(self.insideip)]       # OPT 54
        self.renewtime = [4, 43200]                            # OPT 58
        self.rebindtime = [4, 74025]                           # OPT 59
        self.mtypeopt = []
        self.serveroptions = OrderedDict()
        
        self.serveroptions[54] = self.dhservident
        self.serveroptions[53] = self.mtypeopt

    def Options(self, clientoptions):
        if (51 not in clientoptions):
            self.serveroptions[51] = self.leasetime
        for option in clientoptions:
            if (option in self.optset):                
                optnameindex = self.optnums.index(option)
                optvals = eval('self.{}'.format(str(self.optnames[optnameindex])))
                self.serveroptions[option] = optvals
            else:
                pass
        return self.serveroptions
        
    def Data(self, data):
#        options = []
        options = OrderedDict()
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
        mac = data[28:28+6] # MAC ADDR ONLY
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
        
        if mtype not in {7}:
            paramreq = data[b]
            paramlen = data[b + 1]
            paramitems = data[b + 2:b + 2 + paramlen]
        
            for byte in paramitems:
#                options.append(byte)
                options[byte] = None
        else:
            pass
        
        
        print('MTYPE: {}'.format(mtype))
        return(mtype, xID, mac, ciaddr, chaddr, options)
        
if __name__ == '__main__':
    DHCPServer = DHCPServer()
    DHCPServer.Start()
