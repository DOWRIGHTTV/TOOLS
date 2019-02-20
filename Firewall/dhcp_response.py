#!/usr/bin/python3

import os, time, subprocess
import threading, asyncio
import struct

from socket import *
from config import INIFACE, LOCALNET
from interface_info import Interface

class DHCPResponse:
    def __init__(self, mtype, xid, mac, ciaddr, chaddr, options, Leases):
        self.Leases = Leases
        Int = Interface()
        self.insideip = Int.IP(INIFACE)
        self.mtu = Int.MTU(INIFACE)        
        self.netmask = Int.Netmask(INIFACE) 
        
        self.mtype = mtype
        self.xID = xid
        self.chaddr = chaddr
        self.ciaddr = ciaddr
        self.clientoptions = options

        self.yiaddr = self.Leases.Handout(mac)
        print('Handing Out: {}'.format(self.yiaddr))
    
    def Options(self):
        self.subnetmask = [4, inet_aton(self.netmask)]          # OPT 1
        self.router = [4, inet_aton('192.168.5.1')]             # OPT 3        
#        self.router = [4, inet_aton(self.insideip)]            # OPT 3
        self.dnsserver = [4, inet_aton('192.168.5.1')]          # OPT 6  
#        self.dnsserver = [4, inet_aton(self.insideip)]         # OPT 6
        self.mtu = [2, int(self.mtu)]                           # OPT 26
        self.broadcast = [4, inet_aton('255.255.255.255')]      # OPT 28
        self.leasetime = [4, 86400]                             # OPT 51
        self.dhservident = [4, inet_aton('192.168.5.1')]        # OPT 54
#        self.dhservident = [4, inet_aton(self.insideip)]       # OPT 54
        self.renewtime = [4, 43200]                             # OPT 58
        self.rebindtime = [4, 74025]                            # OPT 59
        self.mtypeopt = [1, self.mtype]                     
        serveroptions = {}
        
        serveroptions[53] = self.mtypeopt
        
        for option in self.clientoptions:
            if option == 1:
                serveroptions[option] = self.subnetmask
            elif option == 3:
                serveroptions[option] = self.router
            elif option == 6:
                serveroptions[option] = self.dnsserver
            elif option == 26:
                serveroptions[option] = self.mtu
            elif option == 28:
                serveroptions[option] = self.broadcast
            elif option == 51:
                serveroptions[option] = self.leasetime
            elif option == 54:
                serveroptions[option] = self.dhservident                
            elif option == 58:
                serveroptions[option] = self.renewtime
            elif option == 59:
                serveroptions[option] = self.rebindtime
            else:
                pass
        self.AssembleOptions(serveroptions)
                
    def AssembleOptions(self, serveroptions):
        self.options = b''
        for option in serveroptions:
            optlen = serveroptions[option][0]
            opt = serveroptions[option][1]
            if (option in {1,3,6,28,54}):
                self.options += struct.pack('!2B', option, optlen) + opt
            elif (option == 26):
                self.options += struct.pack('!2BH', option, optlen, opt)
            elif (option in {51,58,59}):
                self.options += struct.pack('!2BL', option, optlen, opt)
            else:
                self.options += struct.pack('!3B', option, optlen, opt)
        self.options += b'\xFF\x00'
                
    def Assemble(self):
        self.create_dhcp_packet()
        self.assemble_dhcp_packet()
        self.Options()
        
        self.dhcp += self.options
        
        return self.dhcp
        
    def create_dhcp_packet(self):
        self.op         = 2
        self.htype      = 1
        self.hlen       = 6
        self.hops       = 0
        self.xid        = self.xID
        self.secs       = 0
        self.flags      = 0
        self.ciaddr     = inet_aton(self.ciaddr)
        self.yiaddr     = inet_aton(self.yiaddr)
        self.siaddr     = inet_aton(self.insideip)
        self.giaddr     = inet_aton('0.0.0.0')
        
        self.chaddr     = self.chaddr
        self.dnx        = struct.pack('!12s', b'DNX FIREWALL')      
        self.dnxpad     = struct.pack('!52s', b'\x00' * 52)                         
        self.sname      = self.dnx + self.dnxpad
        self.filename     = struct.pack('!128s', b'\x00' * 128)
        self.mcookie    = struct.pack('!4B', 99, 130, 83, 99)                   

    def assemble_dhcp_packet(self):
        self.dhcp = struct.pack('!4B' ,
        self.op,
        self.htype,
        self.hlen,
        self.hops
        )
        self.dhcp += self.xid
        self.dhcp += struct.pack('2H4s4s4s4s',
        self.secs,
        self.flags,
        self.ciaddr,
        self.yiaddr,
        self.siaddr,
        self.giaddr
        )
        self.dhcp += self.chaddr + self.sname + self.filename + self.mcookie
        
