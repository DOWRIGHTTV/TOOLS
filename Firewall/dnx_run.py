#!/usr/bin/python3

import dns_proxy_dev as DNSProxyInit
import dns_relay as DNSServerInit

import multiprocessing
  
def Run():
    DNSProxy = DNSProxyInit.DNSProxy()
    DNSServer = DNSServerInit.DNSServer()
    
    multiprocessing.Process(target=DNSProxy.Start).start()
    multiprocessing.Process(target=DNSServer.Start).start()

       
