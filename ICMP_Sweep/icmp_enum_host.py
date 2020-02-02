#!/usr/bin/python3

import threading
import os, sys
import subprocess

from ipaddress import IPv4Network
from socket import gethostbyname


class EnumHost:
    def __init__(self, file, domain):
        self.file = file
        self.domain = domain
        self.reachable_hosts = []

    def __enter__(self):
        self.devnull = open(os.devnull, 'w')

        return self

    def __exit__(self, exc_type, exc_val, traceback):
        self.devnull.close()
        
        if (exc_type):
            print(exc_val)
            
        return True

    def start(self):
        self.main()
        self.complete()

    def icmp_thread(self, domain):
        try:
            ip_address = gethostbyname(domain)
        except OSError as E:
            return
        
        print(f'pinging ip: {ip_address} for host: {domain}')
        result = subprocess.run(f'ping -c 1 {ip_address}', shell=True, stdout=self.devnull, stderr=self.devnull)
        if (not result.returncode):
            self.reachable_hosts.append(f'{domain} {ip_address}')

    def main(self):
        threads = []
        with open(self.file, 'r') as sd:
            sub_domains = sd.read().split()
            
        for sub_domain in sub_domains:
            fqdn = f'{sub_domain}.{self.domain}'
            thread = threading.Thread(target=self.icmp_thread, args=(fqdn,))
            thread.start()
            threads.append(thread)
            
        for thread in threads:
            thread.join()

    def complete(self):
        if self.reachable_hosts:
            print('||Following Hosts are UP||')
            print('-' * 24)
        else:
            print('NO HOSTS RESPONDED :(.')

        for host in sorted(self.reachable_hosts):
            print(host)

def scan_again():
    while True:
        user_input = input('Do another scan? [Y/n]: ').lower()
        if (user_input in ['y', '']):
            break
        elif (user_input == 'n'):
            exit('exiting...')
        else:
            print('invalid entry. try again.')

def main():
    while True:
        user_input = input('enter domain to enumerate: ')
        enum_file  = input('enter file to load: ')
        with EnumHost(enum_file, user_input) as enum_host:
            enum_host.start()

        scan_again()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit('\nexiting due to keyboard interrupt!')
