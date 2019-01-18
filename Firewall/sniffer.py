#!/usr/bin/python3

import socket
import struct
import binascii
import codecs

class Sniffer:
    def __init__(self, iface, AK):
        self.AK = AK
        self.iface = iface
        self.sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
        self.sock.bind((self.iface, 3))
        
        self.sniffer()
        
    def sniffer(self):
        
        while True:
            self.data, self.addr = self.sock.recvfrom(1600)
            
            packet = Packet(self.data, self.addr)
            
            self.AK(packet)
            
                                        
class Packet:
    def __init__(self, data, addr):
        self.data = data
        self.addr = data
        
        try:  
            self.udp()

            if (self.dport == 53):
                self.dnsQuery()
                self.dns()
            else:
                pass
        
            if (self.qtype == 1):
                self.ip()
                self.ethernet()
               
        except Exception as E:
            pass
                
    def ethernet(self):   
        s = []
        d = []
        smac = struct.unpack('!6c', self.data[0:6])
        dmac = struct.unpack('!6c', self.data[6:12])
        PROTO = struct.unpack('!2c', self.data[12:14])

        for byte in smac:
            s.append(byte.hex())
        for byte in dmac:
            d.append(byte.hex())
    
        self.smac = '{}:{}:{}:{}:{}:{}'.format(s[0], s[1], s[2], s[3], s[4], s[5])
        self.dmac = '{}:{}:{}:{}:{}:{}'.format(d[0], d[1], d[2], d[3], d[4], d[5])
    
    
    def ip(self):
        s = struct.unpack('!4B', self.data[26:30])
        d = struct.unpack('!4B', self.data[30:34])
        self.src = '{}.{}.{}.{}'.format(s[0], s[1], s[2], s[3])
        self.dst = '{}.{}.{}.{}'.format(d[0], d[1], d[2], d[3])

    def udp(self):
        ports = struct.unpack('!2H', self.data[34:38])
        self.sport = ports[0]
        self.dport = ports[1]
    
    def dns(self):
        dnsID = struct.unpack('!H', self.data[42:44])
        self.dnsID = dnsID[0]        

    def dnsQuery(self):
        b = 0
        for byte in self.data[54:]:
            b += 1
        enD = b + 54
        oS = enD - 4
        qL = oS - 55
        dnsQ = struct.unpack('!2H', self.data[oS:enD])   
        self.qtype = dnsQ[0]
        qname = struct.unpack('!{}B'.format(qL), self.data[54:oS - 1])
        len = -1
        self.qname = ''
        for byte in qname:
            if(len == -1):
                len = byte
            elif(len == 0):
                len = byte
                self.qname += "."
            else:
                self.qname += chr(byte)
                len -= 1
               
#Sniffer('eth0', AK=custom_action)

     
        
        
        
        
        
