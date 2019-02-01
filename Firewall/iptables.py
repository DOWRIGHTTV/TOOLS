#!/usr/bin/python3


from subprocess import run, run
from interface_ip import *
from config import *

class IPTables:
    def __init__(self):
        Int = Interface()
        self.insideip = Int.InsideIP()
        self.wanip = Int.WanIP()
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
            run('sudo iptables -N {}'.format(chain), shell=True, check=True)
            run(['sudo iptables -A {} -j RETURN'.format(chain), shell=True)
        
    def main_forward_set(self):
        run('sudo iptables -P FORWARD DROP', shell=True)
        if (EXTERNALDNS == True):
            run('sudo iptables -A FORWARD -p udp --dport 53 -j REJECT', shell=True)
            run('sudo iptables -A FORWARD -p tcp --dport 53 -j REJECT', shell=True)
        elif (EXTERNALDNS == False):
            for chain in self.cChains:
                run('sudo iptables -A FORWARD -p udp --sport 53 -j {}'.format(chain),shell=True)
            for chain in self.cChains:
                run(['sudo iptables -A FORWARD -p udp --dport 53 -j {}'.format(chain), shell=True)
        run('sudo iptables -A FORWARD -i {} -j ACCEPT'.format(INIFACE), shell=True)
        run('sudo iptables -A FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT', shell=True)
        
    def main_input_set(self):
        run('sudo iptables -P INPUT DROP', shell=True)
        for chain in self.cChains:
            run('sudo iptables -A INPUT -p udp --dport 53 -j {}'.format(chain))
        run('sudo iptables -A INPUT -i {} -p icmp --icmp-type any -j ACCEPT'.format(INIFACE), shell=True)
        run('sudo iptables -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT', shell=True)
        run('sudo iptables -A INPUT -i {} -p udp --dport 53 -j ACCEPT'.format(INIFACE), shell=True)
        run('sudo iptables -A INPUT -i {} -p tcp --dport 443 -j ACCEPT'.format(INIFACE), shell=True)
        
    def main_output_set(self):
        run('sudo iptables -P OUTPUT DROP', shell=True)
        run('sudo iptables -A OUTPUT -d {} -j ACCEPT'.format(LOCALNET), shell=True)
        run('sudo iptables -A OUTPUT -s {} -j MALICIOUS'.format(self.wanip), shell=True)
        run('sudo iptables -A OUTPUT -s {} -j ACCEPT'.format(self.wanip), shell=True)
        
    def NAT(self):
        run('sudo iptables -t nat -A POSTROUTING -o {} -j MASQUERADE'.format(WANIFACE), shell=True)
        
        
