#!/usr/bin/python3


from subprocess import run
from interface_ip import *
from config import *

class IPTables:
    def __init__(self):
        Int = Interface()
        self.insideip = Int.IP(INIFACE)
        self.wanip = Int.IP(WANIFACE)
        self.cChains = ['MALICIOUS', 'WHITELIST', 'BLACKLIST']
        
    def Start(self):
        try:
            self.create_new_chains()
            self.main_forward_set()
            self.main_input_set()
            self.main_output_set()
            self.NAT()
        except Exception as E:
            print(E)
            
    def create_new_chains(self):
        for chain in self.cChains:
            run('iptables -N {}'.format(chain), shell=True, check=True) # Creating Custom Chains for use
            run('iptables -A {} -j RETURN'.format(chain), shell=True) # Appending return action to bottom of all custom chains
        
    def main_forward_set(self):
        run('iptables -P FORWARD DROP', shell=True) # Default DROP
        if (EXTERNALDNS == True):
            run('iptables -A FORWARD -p udp --dport 53 -j REJECT', shell=True) # Block External DNS Queries UDP (Public Resolver)
            run('iptables -A FORWARD -p tcp --dport 53 -j REJECT', shell=True) # Block External DNS Queries TCP (Public Resolver)
        elif (EXTERNALDNS == False):
            for chain in self.cChains:
                run('iptables -A FORWARD -p udp --sport 53 -j {}'.format(chain),shell=True) # Return Traffic From External DNS Server
            for chain in self.cChains:
                run('iptables -A FORWARD -p udp --dport 53 -j {}'.format(chain), shell=True) # Initial DNS Request from Internal Host
        run('iptables -A FORWARD -i {} -j ACCEPT'.format(INIFACE), shell=True) # Allowing traffic to go to WAN from Inside Interface
        run('iptables -A FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT', shell=True) # Tracking connection state for return traffic from WAN back to Inside
        
    def main_input_set(self):
        run('iptables -P INPUT DROP', shell=True) # Default DROP
        for chain in self.cChains:
            run('iptables -A INPUT -p udp --dport 53 -j {}'.format(chain), shell=True) # DNS Query pushed to Custom chains for inspection
        run('iptables -A INPUT -i {} -p icmp --icmp-type any -j ACCEPT'.format(INIFACE), shell=True) # Allow ICMP to Firewall
        run('iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT', shell=True) # Tracking connection state for return traffic from WAN back Firewall itself
        run('iptables -A INPUT -i {} -p udp --dport 53 -j ACCEPT'.format(INIFACE), shell=True) # DNS Query( To firewall DNS Relay) is allowed if chains return/do not block
        run('iptables -A INPUT -i {} -p tcp --dport 443 -j ACCEPT'.format(INIFACE), shell=True) # Allowing HTTPS to Firewalls Web server (internal only)
        run('iptables -A INPUT -i {} -p tcp --dport 443 -j ACCEPT'.format(INIFACE), shell=True) # Allowing HTTP to Firewalls Web server (internal only)
                
    def main_output_set(self):
        run('iptables -P OUTPUT DROP', shell=True) # Default DROP
        run('iptables -A OUTPUT -d {} -j ACCEPT'.format(LOCALNET), shell=True) # Allowing all outbound traffic to Inside network
        run('iptables -A OUTPUT -s {} -j MALICIOUS'.format(self.wanip), shell=True) # putting firewall connections through malacious inspection 
        run('iptables -A OUTPUT -s {} -j ACCEPT'.format(self.wanip), shell=True) # allowing all outgoing connections from Firewall (replacing default Allow)
        
    def NAT(self):
        run('iptables -t nat -A POSTROUTING -o {} -j MASQUERADE'.format(WANIFACE), shell=True) # Main masquerade rule. Inside to Outside
        run('echo 1 > /proc/sys/net/ipv4/ip_forward', shell=True) # Allow forwarding through system, required for NAT to work.
        
        
