#!/usr/bin/python3

import re

import threading
import multiprocessing
import asyncio

from config import *

from hakcbot_init import Hakcbot as Hbot
from hakcbot_execute import Execute
from hakcbot_spam import Spam

class Run:
    def __init__(self, Hakcbot):
        self.Hakcbot = Hakcbot
        self.Execute = Execute(self.Hakcbot)
        self.Automate = Automate(self.Hakcbot)
        self.Spam = Spam(self.Hakcbot)
        
        self.linecount = 0
        
    def Processes(self):
#        multiprocessing.Process(target=self.Hakc).start()
#        multiprocessing.Process(target=self.Hakc2).start()
        
        threading.Thread(target=self.Hakc).start()
        threading.Thread(target=self.Hakc2).start()
            
    def Hakc(self):
        rb = ''
        try:
            while True:
                rb = rb + self.Hakcbot.s.recv(1024).decode('utf-8', 'ignore')
                chat = rb.split('\n')
                rb = chat.pop()
                        
                for line in chat:
                    if ('PING :tmi.twitch.tv\r' == line):
                        print(line)
                        self.linecount = 0
                        self.Hakcbot.s.send('PONG :tmi.twitch.tv\r\n'.encode("utf-8"))
                    elif ('JOIN' in line):
                        pass
                    else:
                        spam = self.Spam.Main(line)
                        if (not spam):
                            self.Execute.Main(line)
                            self.linecount += 1
                            self.Automate.linecount = self.linecount
                        else:
                            pass
                            
        except Exception as E:
            print('Main Process Error: {}'.format(E))

    
    def Hakc2(self):
        key = ['Sub', 'Commands', 'Discord', 'Github']
        value = [60, 50, 45, 30]
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(asyncio.gather(
            self.Automate.Timers(key[0], value[0]),
            self.Automate.Timers(key[1], value[1]),
            self.Automate.Timers(key[2], value[2]),
            self.Automate.Timers(key[3], value[3])))
            
        except Exception as E:
            print('AsyncIO General Error')
            
class Automate:
    def __init__(self, Hakcbot):
        self.Execute = Execute(Hakcbot)
        
        self.linecount = 0
                
    async def Timers(self, key, value):
        try:
            while True:
                await asyncio.sleep(60 * value)
                if (self.linecount >= 3):
                    eval('self.Execute.{}()'.format(key))
                else:
                    pass
        except Exception as E:
            print('AsyncIO Timer Error')
            
class Main:
    def __init__(self):
        Hakcbot = Hbot()
        Hakcbot.Connect()
        HakcbotRun = Run(Hakcbot)
        HakcbotRun.Processes()
     
Main()



