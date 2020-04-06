#!/usr/bin/python3

import os, sys
import time
import threading

from subprocess import run, SubprocessError, DEVNULL
from ipaddress import IPv4Network


class PingSweep:
    def __init__(self, subnet):
        self._subnet = subnet
        self._reachable_hosts = []

        self._ip_count        = 0
        self._completed_count = 0
        self._counter_lock    = threading.Lock()
        self._sweep_complete  = threading.Event()

    def __enter__(self):
        try:
            self._ip_network = list(IPv4Network(self._subnet).hosts())
        except Exception:
            self._ip_network = None
        else:
            self._ip_count = len(self._ip_network)

        return self

    def __exit__(self, exc_type, exc_val, traceback):
        return True

    def start(self):
        if (self._ip_network is None):
            raise TypeError('invalid network subnet. ex. 192.168.100.0/24')

        threading.Thread(target=self._main).start()
        # blocking until all threads finished and completion event is set
        self._timer(time.time())
        self._complete()

    def _icmp(self, ip_address):
        try:
            run(f'ping -c 1 -W 0.51 {ip_address}',
                shell=True, check=True, stdout=DEVNULL, stderr=DEVNULL)
        except SubprocessError:
            pass
        else:
            self._reachable_hosts.append(ip_address)

        with self._counter_lock:
            self._completed_count += 1
            self._progress()

    def _main(self):
        threads = []
        for ip_address in self._ip_network:
            threads.append(threading.Thread(target=self._icmp, args=(ip_address,)))

        # starting all threads. 1 for each host.
        for thread in threads:
            thread.start()
        # waiting for all threads to complete
        for thread in threads:
            thread.join()

        self._sweep_complete.set()

    def _complete(self):
        print('\n' + '-' * 26)
        print(f'completed in {self._time_to_sweep} seconds')
        print('-' * 26)
        if (not self._reachable_hosts):
            print('NO HOSTS RESPONDED :(.')
        else:
            for ip in self._reachable_hosts:
                print(str(ip))

    def _timer(self, start):
        self._sweep_complete.wait()

        self._time_to_sweep = round(time.time() - start, 2)

    def _progress(self):
	    bar_len = 38
	    filled_len = int(round(bar_len * self._completed_count / float(self._ip_count)))
	    percents = round(100.0 * self._completed_count / float(self._ip_count), 1)
	    bar = '#' * filled_len + '=' * (bar_len - filled_len)
	    sys.stdout.write(f'{self._completed_count}/{self._ip_count} || [{bar}] {percents}%s\r')
	    sys.stdout.flush()

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
        ip_range = input('IP range to scan: ')
        with PingSweep(ip_range) as ping_sweep:
            ping_sweep.start()

        scan_again()

if __name__ == '__main__':
    print('Ping sweep| by DOWRIGHT. ^_^')
    print('-' * 26)
    main()
