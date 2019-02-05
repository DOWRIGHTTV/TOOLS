#!/usr/bin/python3

import multiprocessing
import threading

import dns_proxy_dev as DNSProxyInit
import dns_relay as DNSRelayInit

  
def Run():
    DNSProxy = DNSProxyInit.DNSProxy()
    DNSRelay = DNSRelayInit.DNSRelay()

#    multiprocessing.Process(target=DNSProxy.Start).start()
#    multiprocessing.Process(target=DNSRelay.Start).start()
 
    
    threading.Thread(target=DNSProxy.Start).start()
    threading.Thread(target=DNSRelay.Start).start()

       
