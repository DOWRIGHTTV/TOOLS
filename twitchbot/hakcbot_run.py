#!/usr/bin/python3

import threading, asyncio
import re, json

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
                        self.Automate.linecount = self.linecount
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
        cmd = ['Sub', 'Commands', 'Discord', 'Github']
        timer = [99, 87, 59, 47]
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(asyncio.gather(
            self.Automate.Timers(cmd[0], timer[0]),
            self.Automate.Timers(cmd[1], timer[1]),
            self.Automate.Timers(cmd[2], timer[2]),
            self.Automate.Timers(cmd[3], timer[3])))
            
        except Exception as E:
            print('AsyncIO General Error')
            
class Automate:
    def __init__(self, Hakcbot):
        self.Execute = Execute(Hakcbot)
        
        self.linecount = 0
        
        with open('commands.json', 'r') as cmds:
            self.commands = json.load(cmds)
                
    async def Timers(self, cmd, timer):
        try:
            message = self.commands[cmd]['message']
            while True:
                await asyncio.sleep(60 * timer)
                print('Line Count: {}'.format(self.linecount))
                if (self.linecount >= 3):
                    self.Execute.sendMessage(message)
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

if __name__ == '__main__':
    try:  
        Main()
    except KeyboardInterrupt:
        print('Exiting Hakcbot :(')



