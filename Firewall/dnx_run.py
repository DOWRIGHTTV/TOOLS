#!/usr/bin/python3

import multiprocessing
import threading

import dns_proxy_dev as DNSProxyInit
import dns_relay as DNSRelayInit
import dhcp_server as DHCPServerInit

  
def Run():
    DNSProxy = DNSProxyInit.DNSProxy()
    DNSRelay = DNSRelayInit.DNSRelay()
    DHCPServer = DHCPServerInit.DHCPServer()
#    multiprocessing.Process(target=DNSProxy.Start).start()
#    multiprocessing.Process(target=DNSRelay.Start).start()
 
    
    threading.Thread(target=DNSProxy.Start).start()
    threading.Thread(target=DNSRelay.Start).start()
    threading.Thread(target=DHCPServer.Start).start()
       
