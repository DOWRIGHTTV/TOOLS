#!/usr/bin/python3

import time
import random
import threading
import os, sys
import subprocess

from ipaddress import IPv4Network


class PingSweep:
    def __init__(self, subnet):
        try:
            self.ip_network = IPv4Network(subnet).hosts()
        except Exception:
            raise TypeError('invalid network subnet. ex. 192.168.100.0/24')

        self.reachable_hosts = []

    def __enter__(self):
        self.devnull = open(os.devnull, 'w')
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        self.devnull.close()

    def start(self):
        self.main()
        self.complete()

    def thread_handler(self, ip_address):
        error = self.icmp_worker(ip_address)
        if (not error):
            self.reachable_hosts.append(ip_address)

    def icmp_worker(self, ip_address):
        result = subprocess.run(f'ping -c 1 {ip_address}', shell=True, stdout=self.devnull, stderr=self.devnull)
        return result.returncode

    def main(self):
        for ip_address in self.ip_network:
            threading.Thread(target=self.thread_handler, args=(ip_address,)).start()

    def complete(self):
        if self.reachable_hosts:
            print('||FOLLOWING IPs ARE UP||')
            print('-' * 24)
        else:
            print('NO HOSTS RESPONDED :(.')

        for ip_address in sorted(self.reachable_hosts):
            print(ip_address)

def scan_again():
    while True:
        user_input = input('Do another scan? [Y/n]: ').lower()
        if (user_input in ['y', '']):
            break
        elif (user_input == 'n'):
            os._exit(0)
        else:
            print('invalid entry. try again.')

def main():
    while True:
        user_input = input('IP Range to scan: ')
        try:
            with PingSweep(user_input) as ping_sweep:
                ping_sweep.start()
        except TypeError as e:
            print(e)
        else:
            scan_again()

if __name__ == '__main__':
    main()
