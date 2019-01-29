#!/usr/bin/python3

import dns_proxy_dev as DNSProxyInit
import dns_serv as DNSServerInit

import multiprocessing



  
def Run(self):
    DNSProxy = DNSProxyInit()
    DNSServer = DNSServerInit()
    
    multiprocessing.Process(target=DNSProxy.Start).start()
    multiprocessing.Process(target=DNSServer.Start).start()

       
