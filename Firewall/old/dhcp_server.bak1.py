#!/usr/bin/python3



from socket import *

from config import INIFACE
from interface_ip import Interface

class DHCPServer:
    def __init__(self):
        Int = Interface()
        self.insideip = Int.IP(INIFACE)       

    def Start(self):
        print("DHCP server is starting...\n")        
        self.s = socket(AF_INET, SOCK_DGRAM)
#        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
        self.s.setsockopt(SOL_SOCKET, SO_BROADCAST,1)
        self.s.bind(('0.0.0.0', 67))
        print("Listening on 0.0.0.0:67")        
        while True:
            try:
                self.rdata, self.addr = self.s.recvfrom(1024)
                mtype, xID, chaddr, options = self.Parse(self.rdata)
                if mtype == b'\x01':
                    threading.Thread(target=self.Response, args=(2, self.insideip, xID, chaddr, options,)).start()
                elif mtype == b'\x03':
                    threading.Thread(target=self.Response, args=(5, self.insideip, xID, chaddr, options,)).start()
            except Exception as LOL:
                print(LOL)    
#    def Response(self, option, xid, chaddr):
#        Packet = DHCPPacket(self.insideip, option, xid, chaddr)
#        self.sdata = Packet.Assemble()
        
#        s = socket(AF_INET, SOCK_DGRAM)
#        self.s.sendto(self.sdata, self.addr)

    def Parse(self, data):
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

        paramreq = data[b]
        paramlen = data[b + 1]
        paramitems = data[b + 2:b + 2 + paramlen]
        
        for byte in paramitems:
            item = paramitems[i]
            options.append(item)
        
        return(mtype, xID, chaddr, options)
        
        

class DHCPRespond:
    def __init__(self, insideip, mtype, xid, chaddr, options):
        self.insideip = insideip
        self.mtype = mytpe
        self.xID = xid
        self.CHaddr = chaddr
        self.clientoptions = options

    
    def Options(self):
        self.subnetmask = [4, inet_aton('255.255.255.0')]
        self.router = [4, inet_aton(self.insideip)]
        self.dnsserver = [4, inet_aton(self.insideip)]
        self.leasetime = [4, 86400]
        self.serveroptions = {}
        
        [1, 3, 6, 15, 26, 28, 51, 58, 59, 43]
        
        for option in self.clientoptions:
            if option == 1:
                serveroptions[option] = self.subnetmask
            elif option == 3:
                serveroptions[option] = self.router
            elif option == 6:
                serveroptions[option] = self.dnsserver
            elif option == 51:
                serveroptions[option] = self.leasetime
            else:
                serveroptions[option] = [1, 0]
                
    def AssembleOptions(self):
        self.option = ''
        for option in self.serveroptions:
            optlen = self.serveroption[option][0]
            opt = self.serveroption[option][1]
            self.option += struct.pack('!2B{}B'.format(optlen), option, optlen, opt)
    


    def Assemble(self):
        self.create_dhcp_packet()
        self.assemble_dhcp_packet()
        
        return self.dhcp
        
    def create_dhcp_packet(self):
        self.op         = 2
        self.htype      = 1
        self.hlen       = 6
        self.hops       = 0
        self.xid        = self.xID
        self.secs       = 1
        self.flags      = 0
        self.ciaddr     = 0
        self.yiaddr     = inet_aton('192.168.83.26')
        self.siaddr     = inet_aton(self.insideip)
        self.giaddr     = 0
        self.chaddr     = self.CHaddr
        self.dnx        = struct.pack('!12B', 'DNX FIREWALL')                   # b'\x44\x4e\x58\x20\x46\x49\x52\x45\x57\x41\x4c\x4c'
        self.dnxpad     = struct.pack('!52B', '0' * 52)                         # b'\x00' * 52
        self.sname      = self.dnx + self.dnxpad
        self.mcookie    = struct.pack('!4B', 99, 130, 83, 99)                   # b'\x63\x82\x53\x63'
        self.option     = struct.pack('!3B', 53, 1, self.mtype)                # b'\x35\x01' + struct.pack('!B', self.option) #53 , 1 , 2
        self.option2    = struct.pack('!6B', 1, 4, inet_aton('255.255.255.0'))  # b'\x01\x04' + struct.pack('!4B', inet_aton('255.255.255.0')) #1, 4, inet_aton('255.255.255.0')
        self.option3    = struct.pack('!6B', 3, 4, inet_aton(self.insideip))    # b'\x03\x04' + struct.pack('!4B', inet_aton(self.insideip)) #3, 4, inet_aton('192.168.83.4')
        self.option4    = struct.pack('!2BL', 51, 4, 86400)                     # b'\x33\x04' + b'\x00\x01\x51\x80' #51, 4, b'\x00\x01\x51\x80'
        self.option5    = struct.pack('!6B', 54, 4, inet_aton(self.insideip))   # b'\x36\x04' + struct.pack('!4B', inet_aton(self.insideip)) #54, 4, inet_aton('192.168.83.4')
        self.dhcp2      = self.chaddr2 + self.sname + self.mcookie + self.option + self.option2 + self.option3 + self.option4 + self.option5

    def assemble_dhcp_packet(self):
        self.dhcp = struct.pack('!4BL2H4L' ,
        self.op,
        self.htype,
        self.hlen,
        self.hops,
        self.xid,
        self.secs,
        self.flags,
        self.ciaddr,
        self.yiaddr,
        self.siaddr,
        self.giaddr,
        self.chaddr1
        )
        self.dhcp += dhcp2

if __name__ == '__main__':
    DHCPServer = DHCPServer()
    DHCPServer.Start()
