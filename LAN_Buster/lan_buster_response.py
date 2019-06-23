#!/usr/bin/env python3

import os, sys, time, subprocess
import threading, asyncio
import struct

from socket import inet_aton

class DHCPRequest:
    def __init__(self, mac, xID, mtype, assigned_ip='0.0.0.0'):
        self.mac = mac
        self.xID = xID
        self.mtype = mtype
        self.assigned_ip = assigned_ip

    def Request(self):
        self.CreateDHCP()
        self.AssembleDHCP()
        self.CreateOptions()
        self.AssembleOptions()

        dhcp_packet = self.dhcp_request + self.dhcp_options

        return dhcp_packet
        
    def CreateDHCP(self):
        self.op         = 1
        self.htype      = 1
        self.hlen       = 6
        self.hops       = 0
        self.xid        = self.xID
        self.secs       = 0
        self.flags      = (1 << 15) | (0 << 14)
        self.ciaddr     = inet_aton(self.assigned_ip)
        self.yiaddr     = 0
        self.siaddr     = 0
        self.giaddr     = 0
        
        self.chaddr     = self.mac + struct.pack('!10s', b'\x00' * 10)
        self.request_pad     = struct.pack('!64s', b'\x00' * 64)                         
        self.filename     = struct.pack('!128s', b'\x00' * 128)
        self.mcookie    = struct.pack('!4B', 99, 130, 83, 99)                   

    def AssembleDHCP(self):
        self.dhcp_request = struct.pack('!4B' ,
        self.op,
        self.htype,
        self.hlen,
        self.hops
        )
        self.dhcp_request += self.xid
        self.dhcp_request += struct.pack('!2H4s3L',
        self.secs,
        self.flags,
        self.ciaddr,
        self.yiaddr,
        self.siaddr,
        self.giaddr
        )
        
        self.dhcp_request += self.chaddr + self.request_pad + self.filename + self.mcookie

    def CreateOptions(self):
        self.opt_53 = 53
        self.opt_53_len = 1
        self.opt_53_type = self.mtype

        if (self.mtype == 1):
            option = 55
            params = [1, 3, 6, 28]
            self.opt_55 = [option, len(params), params]

        elif (self.mtype == 4):
            self.opt_50 = 50
            self.opt_50_len = 4
            self.opt_50_ip = inet_aton(self.assigned_ip)

    def AssembleOptions(self):
        self.dhcp_options = struct.pack('!3B',
        self.opt_53,
        self.opt_53_len,
        self.opt_53_type
        )
        if (self.mtype == 1):
            self.dhcp_options += struct.pack('!2B',
            self.opt_55[0],
            self.opt_55[1]
            )

            for value in self.opt_55[2]:
                self.dhcp_options += struct.pack('!B', value)

        # elif (self.mtype == 4):
        #     self.dhcp_options += struct.pack('!2B',
        #     self.opt_50,
        #     self.opt_50_len,
        #     self.assigned_ip
        #     )

        self.dhcp_options += b'\xff'
            