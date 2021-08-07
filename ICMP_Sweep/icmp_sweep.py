#!/usr/bin/python3

import os, sys
import time
import threading

from subprocess import run, SubprocessError, DEVNULL
from ipaddress import IPv4Network
from functools import partial

_stdout_write = sys.stdout.write
_stdout_flush = sys.stdout.flush

_thread_limit = threading.BoundedSemaphore(value=25)

shell = partial(run, shell=True, check=True, stdout=DEVNULL, stderr=DEVNULL)

# Windows/Linux ping arg swap..
if (os.name == 'posix'):
    count, timeout = '-c 1', '-W 1'

else:
    count, timeout = '-n 1', '-w 1000'
    print('Windows detected, adjusting Ping args.')


class PingSweep:

    __slots__ = (
        '_ip_network', '_ip_count', '_completed_count',

        '_counter_lock', '_sweep_complete', '_reachable_hosts',
        '_time_to_sweep',
    )

    def __init__(self, subnet):
        try:
            self._ip_network = list(IPv4Network(subnet).hosts())
        except Exception:
            raise TypeError('invalid network subnet. ex. 192.168.100.0/24')

        self._ip_count = len(self._ip_network)
        self._completed_count = 0
        self._counter_lock    = threading.Lock()
        self._sweep_complete  = threading.Event()

        self._reachable_hosts = []

    def run(self):

        threading.Thread(target=self._sweep).start()

    def wait(self, start):
        self._sweep_complete.wait()

        self._time_to_sweep = round(time.time() - start, 2)
	
    def report(self):
        print('\n' + '-' * 26)
        print(f'completed in {self._time_to_sweep} seconds')
        print('-' * 26)
        if (not self._reachable_hosts):
            print('NO HOSTS RESPONDED :(.')

        else:
            for ip in self._reachable_hosts:
                print(f'{ip}')

    def _sweep(self):
        threads = []
        for ip_address in self._ip_network:
            threads.append(threading.Thread(target=self._icmp, args=(ip_address,)))

        # starting all threads. 1 for each host.
        for thread in threads:
            thread.start()

        # waiting for all threads to complete
        for thread in threads:
            thread.join()

        self._time_to_sweep = time.time()
        self._sweep_complete.set()

    def _icmp(self, ip_address):
        with _thread_limit:
            try:
                shell(f'ping {count} {timeout} {ip_address}')
            except SubprocessError as se:
                print(se)

            else:
                self._reachable_hosts.append(ip_address)

            with self._counter_lock:
                self._progress()

    def _progress(self):
        self._completed_count += 1

        bar_len = 38
        filled_len = int(round(bar_len * self._completed_count / float(self._ip_count)))
        percents = round(100.0 * self._completed_count / float(self._ip_count), 1)
        bar = '#' * filled_len + '=' * (bar_len - filled_len)

        _stdout_write(f'{self._completed_count}/{self._ip_count} || [{bar}] {percents}%s\r')
        _stdout_flush()

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

        try:
            ps = PingSweep(ip_range)
        except TypeError as te:
            print(te)
            continue

        except Exception as e:
            print(f'unexpected error: {e}')
            continue

        ps.run()

        # blocking call that will return when all ips have been scanned.
        ps.wait(time.time())

        # print results of scan
        ps.report()

        scan_again()

if __name__ == '__main__':
    print(f'Ping sweep| by DOWRIGHT. ^_^\n{"-" * 26}')
    main()

		
