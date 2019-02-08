#!/usr/bin/python3

import struct
import threading
from socket import *

from config import INIFACE, LOCALNET
from interface_ip import Interface

class DHCPServer:
    def __init__(self):
        Int = Interface()
        self.insideip = Int.IP(INIFACE)
        
        self.Lease = DHCPLeases()

    def Start(self):
        print("DHCP server is starting...\n")
        
        #--Creating Lease Dictionary--#
        self.Leases.BuildRange()
        
        #Loading Lease Expiration Timer--##
        threading.Thread(target=self.Lease.Timer).start()
        
        #--Creating Sockets--##
        
        self.s = socket(AF_INET, SOCK_DGRAM)
#        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
        self.s.setsockopt(SOL_SOCKET, SO_BROADCAST,1)
        self.s.bind(('0.0.0.0', 67))
        print("[+] Listening on Port 67")        
        while True:
            try:
                self.rdata, self.addr = self.s.recvfrom(1024)
                addr, port = self.addr
                print('Received {}:{}'.format(addr, port))
                print(self.rdata)
                mtype, xID, chaddr, options, requestedip = self.Parse(self.rdata)
                if mtype == 1: #b'\x01':
                    threading.Thread(target=self.Response, args=(2, xID, chaddr, options,)).start()
                elif mtype == 3: #b'\x03':
                    threading.Thread(target=self.Response, args=(5, xID, chaddr, options,)).start()
            except Exception as LOL:
                print(LOL)
                
    def Response(self, mtype, xID, chaddr, options):
        Response = DHCPResponse(mtype, xID, chaddr, options, requestedip)
        sdata = Response.Assemble()
        
        print('Responding with TYPE: {}'.format(mtype))
#        print(sdata)
        print('Sent {}:{}'.format('255.255.255.255', 68))
        self.s.sendto(sdata, ('255.255.255.255', 68))

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
#        chaddr = data[28:28+6] # MAC ONLY
        chaddr = data[28:28+16]
        mcookie = data[236:240]
        dhcpm = data[240]
        mlen = data[241]
        mtype = data[242]
        
#        rip = None

#        if mtype == 3:
#            b2 = 0
#            z = 0
#            for byte in data:
#                b2 += 1
#                currentbyte = data[b2 - 1]
#                if (z == 0 and currentbyte == 50):
#                    optlen = data[b2]
#                    requestedip = data[b2 + 1:b2 + 1 + optlen]
#                    ripend = b2 + 1 + optlen
#                    z += 1
#                    rip = struct.unpack('!4B', requestedip)
#                    rip = '{}.{}.{}.{}'.format(rip[0], rip[1], rip[2], rip[3])
                    
        paramreq = data[b]
        paramlen = data[b + 1]
        paramitems = data[b + 2:b + 2 + paramlen]
        
        for byte in paramitems:
#            item = paramitems[i]
            options.append(byte)
        
        print('MTYPE: {}'.format(mtype))
#        print('xID: {}'.format(xID))
#        print('CHADDR: {}'.format(chaddr))
#        print('OPTIONS: {}'.format(options))
        return(mtype, xID, chaddr, options)
        
class DHCPLeases:
    def __init__(self):
        self.leasetable = {}
        bob = LOCALNET.split(.)
        self.iprange = '{}.{}.{}'.format(bob[0], bob[1], bob[2])        
        
    def BuildRange(self): 
        timestamp = time.time()                
        for i in range(16,221)
            hostip = '{}.{}'.format(self.iprange, i))
            response = threading.Thread(target=self.ICMPSweep, args=(hostip,)).start()
            if (response == 0):
                self.leasetable['{}.{}'.format(self.iprange, i)] = timestamp
            else:                
                self.leasetable['{}.{}'.format(self.iprange, i)] = ''
    
    def ICMPSweep(self):
        DEVNULL = open(os.devnull, 'wb')
        res = subprocess.call(['ping', '-c', '1', str(target)], stdout = DEVNULL)	
        return(res)        
        
    def Timer(self):
        while True:
            for ip, value in self.leasetable.items():
                if (value is None):
                    pass
                else:
                    timestamp = time.time()
                    time_elapsed = timestamp - value
                    if (time_elapsed >= 86800):
                        self.leasetable[ip] = ''
                    else:
                        pass
            time.sleep(5 * 60)
    
    def Handout(self):               
        for ip, value in self.leasetable.items():
            if value = None
                timestamp = time.time()
                self.leasetable[ip] = timestamp
                return ip
            else:
                pass
        else:
            return None
        
class DHCPResponse:
    def __init__(self, mtype, xid, chaddr, options) #, requestedip=None):
        Leases = DHCPLeases()
        Int = Interface()
        self.insideip = Int.IP(INIFACE)
        self.mtu = Int.MTU(INIFACE)
        
#        self.insideip = insideip
        self.mtype = mtype
        self.xID = xid
        self.CHaddr = chaddr
        self.clientoptions = options
        
        self.yiaddr = Leases.Handout()

    
    def Options(self):
        self.subnetmask = [4, inet_aton('255.255.255.0')]       # OPT 1
        self.router = [4, inet_aton(self.insideip)]             # OPT 3
        self.dnsserver = [4, inet_aton(self.insideip)]          # OPT 6
        self.mtu = [2, int(self.mtu)]                           # OPT 26
        self.broadcast = [4, inet_aton('255.255.255.255')]      # OPT 28
        self.leasetime = [4, 86400]                             # OPT 51
        self.renewtime = [4, 82800]                             # OPT 58
        self.rebindtime = [4, 84600]                            # OPT 59
        serveroptions = {}
        
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
            elif option == 58:
                serveroptions[option] = self.renewtime
            elif option == 59:
                serveroptions[option] = self.rebindtime
            else:
                serveroptions[option] = [1, 0]
        print(serveroptions)       
        self.AssembleOptions(serveroptions)
                
    def AssembleOptions(self, serveroptions):
        self.options = b''
        for option in serveroptions:
            optlen = serveroptions[option][0]
            opt = serveroptions[option][1]
            print('{} : {} : {}'.format(option, optlen, opt))
            if (option in {1,3,6,28}):
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
        self.secs       = 1
        self.flags      = 0
        self.ciaddr     = inet_aton('0.0.0.0')
        self.yiaddr     = inet_aton(self.yiaddr)
        self.siaddr     = inet_aton(self.insideip)
        self.giaddr     = inet_aton('0.0.0.0')
        
        self.chaddr     = self.CHaddr
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
        
if __name__ == '__main__':
    DHCPServer = DHCPServer()
    DHCPServer.Start()
