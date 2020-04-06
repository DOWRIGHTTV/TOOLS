#!/usr/bin/python3

import os, sys
import time
import threading

import argparse
from sys import argv

from ipaddress import IPv4Network
from socket import gethostbyname
from subprocess import run, CalledProcessError, DEVNULL

parser = argparse.ArgumentParser(description = 'resolves then pings enumerated domain names.')
parser.add_argument('-v', '--verbose', help='prints output to screen', action='store_true')
parser.add_argument('-c', '--clear', help='clears shell throughout, including on startup, automatically.', action='store_true')

args = parser.parse_args(argv[1:])
VERBOSE = args.verbose
CLEAR = args.clear


class EnumHost:
    def __init__(self, file, domain):
        self._file = file
        self._domain = domain
        self._reachable_hosts = []

        self._sweep_complete = threading.Event()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if (exc_type):
            print(exc_val)

        return True

    def start(self):
        threading.Thread(target=self._main).start()

        self._timer(time.time())
        self._complete()

    def _icmp_thread(self, domain):
        try:
            ip_address = gethostbyname(domain)
        except OSError:
            if (VERBOSE):
                print(f'dns failure: {domain}.')
            return

        if (VERBOSE):
            print(f'pinging ip: {ip_address} for host: {domain}')
        try:
            run(f'ping -c 1 -W .51 {ip_address}',
                shell=True, check=True, stdout=DEVNULL, stderr=DEVNULL)
        except CalledProcessError:
            pass
        else:
            self._reachable_hosts.append(f'{domain} {ip_address}')

    def _main(self):
        with open(self._file, 'r') as sd:
            sub_domains = sd.read().split()

        threads = []
        for sub_domain in sub_domains:
            fqdn = f'{sub_domain}.{self._domain}'
            threads.append(threading.Thread(target=self._icmp_thread, args=(fqdn,)))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        self._sweep_complete.set()

    def _complete(self):
        print(f'completed in {self._time_to_sweep} seconds')
        print('-' * 26)
        if not self._reachable_hosts:
            print('NO HOSTS RESPONDED :(.')
        else:

            for host in sorted(self._reachable_hosts):
                print(host)

    def _timer(self, start):
        self._sweep_complete.wait()

        self._time_to_sweep = round(time.time() - start, 2)

def scan_again():
    while True:
        user_input = input('Do another scan? [Y/n]: ').lower()
        if (user_input in ['y', '']):
            break
        elif (user_input == 'n'):
            print('exiting...')
            os._exit(0)
        else:
            print('invalid entry. try again.')

def main():
    while True:
        user_input = input('enter domain to enumerate: ')
        while True:
            enum_file  = input('enter file to load: ')
            if (os.path.isfile(enum_file)): break

            print(f'file {enum_file} does not exist. try again.')

        if (CLEAR):
            run('clear', shell=True)
        with EnumHost(enum_file, user_input) as enum_host:
            enum_host.start()

        scan_again()

if __name__ == '__main__':
    print('Enumerated host name reachability test| by DOWRIGHT. ^_^')
    try:
        if (CLEAR):
            run('clear', shell=True)
        main()
    except KeyboardInterrupt:
        exit('\nexiting due to keyboard interrupt!')
