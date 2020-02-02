#!/usr/bin/python3

import time
import random
import threading
import os, sys
import subprocess

from ipaddress import IPv4Network
from copy import copy


class PingSweep:
    def __init__(self, subnet):
        self.subnet = subnet
        self.reachable_hosts = []
        
        self.ip_count        = 0
        self.completed_count = 0
        self.sweep_complete  = False
        self.counter_lock    = threading.Lock()

    def __enter__(self):
        self.devnull = open(os.devnull, 'w')
        try:
            self.ip_network = list(IPv4Network(self.subnet).hosts())
        except Exception as E:
            self.ip_network = None
        else:
            self.ip_count = len(self.ip_network)

        return self

    def __exit__(self, exc_type, exc_val, traceback):
        self.devnull.close()
        
        return True

    def start(self):
        if (not self.ip_network):
            raise TypeError('invalid network subnet. ex. 192.168.100.0/24')
            
        threading.Thread(target=self._main).start()
        # blocking until all threads finished and completion boolean is set to true
        self._timer(time.time())
        self._complete()

    def _icmp(self, ip_address):
        result = subprocess.run(f'ping -c 1 -W 1 {ip_address}', shell=True, stdout=self.devnull, stderr=self.devnull)
        if (not result.returncode):
            self.reachable_hosts.append(ip_address)
            
        with self.counter_lock:
            self.completed_count += 1
            self._progress()
        
    def _main(self):
        threads = []
        for ip_address in self.ip_network:
            icmp = threading.Thread(target=self._icmp, args=(ip_address,))
            icmp.start()
            threads.append(icmp)

        for thread in threads:
            thread.join()

        self.sweep_complete = True

    def _complete(self):
        print('\n' + '-' * 26)
        print(f'completed in {self.time_to_sweep} seconds')
        if (self.reachable_hosts):
            print('||Following IPs are UP||')
            print('-' * 26)
        else:
            print('NO HOSTS RESPONDED :(.')

        for ip_address in sorted(self.reachable_hosts):
            print(ip_address)
            
    def _timer(self, start):
        while True:
            if (self.sweep_complete):
                self.time_to_sweep = round(time.time() - start, 2)
                break
            
            time.sleep(.001)
            
    def _progress(self):
	    bar_len = 38
	    filled_len = int(round(bar_len * self.completed_count / float(self.ip_count)))
	    percents = round(100.0 * self.completed_count / float(self.ip_count), 1)
	    bar = '#' * filled_len + '=' * (bar_len - filled_len)
	    sys.stdout.write(f'{self.completed_count}/{self.ip_count} || [{bar}] {percents}%s\r')
	    sys.stdout.flush()

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
        ip_range = input('IP range to scan: ')
        with PingSweep(ip_range) as ping_sweep:
            ping_sweep.start()

        scan_again()

if __name__ == '__main__':
    main()
