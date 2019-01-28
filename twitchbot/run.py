#!/usr/bin/python3

from socket import *
from config import *
import re
import sched, time

#import threading
import multiprocessing
import asyncio
import time

uList = []

class Hakcbot_Init:
    def __init__(self):
        self.s = socket()
        self.openSocket()
        self.joinRoom()        
        
    
    def openSocket(self):
        self.s.connect((HOST, PORT))
        self.s.send('PASS {}\r\n'.format(PASS).encode("utf-8"))
        self.s.send('NICK {}\r\n'.format(IDENT).encode("utf-8"))
        self.s.send('JOIN #{}\r\n'.format(CHANNEL).encode("utf-8"))
        
    def joinRoom(self):
        rb = ''
        Loading = True
        while Loading:
            rb = rb + self.s.recv(1024).decode()
            temp = rb.split('\n')
            rb = temp.pop()
            
            for line in temp:
                print(line)
                if ('End of /NAMES list' in line):
                    Loading = False
                else:
                    pass
#        self.sendMessage('Successfully connected to chat!')
        
    def sendMessage(self, message):
        mT = 'PRIVMSG #{} :{}'.format(CHANNEL, message)
        self.s.send('{}\r\n'.format(mT).encode("utf-8"))
 
class Hakcbot_Run:
    def __init__(self, hI):
        self.hI = hI 
        
        self.Hakc_Threads()
        
    def Hakc_Threads(self):
        p1 = multiprocessing.Process(target=self.Hakc)
        p2 = multiprocessing.Process(target=self.Hakc2)

        p1.start()
        p2.start()

            
    def Hakc(self):
        rb = ''
        while True:
            rb = rb + self.hI.s.recv(1024).decode()
            chat = rb.split('\n') 
            rb = chat.pop()
                    
            for line in chat:
                if ('PING :tmi.twitch.tv' == line):                    
                    print(line)
                    self.hI.s.send('PONG :tmi.twitch.tv\r\n'.encode("utf-8"))
                else:
                     hE = Hakcbot_Execute(self.hI, line)
                     hE.Execute()
    
    def Hakc2(self):
        hE = Hakcbot_Execute(self.hI, 'X')
        HbA = Hakcbot_Automate(self.hI, hE)
        key = ['Commands', 'Discord', 'Github']
        value = [50, 45, 30]
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(asyncio.gather(HbA.Timers(key[0], value[0]), HbA.Timers(key[1], value[1]), HbA.Timers(key[2], value[2])))
            
        except Exception as E:
            print(E)
            
class Hakcbot_Automate:
    def __init__(self, hI, hE):
        self.hI = hI
        self.hE = hE
                
    async def Timers(self, key, value):
        #Commands#
        try:
            while True:
                await asyncio.sleep(60 * value)
                eval('self.hE.{}()'.format(key))

        except Exception as E:
            print(E)                       

class Hakcbot_Execute:
    def __init__(self, hI, line):
        self.line = line
        self.hI = hI
        self.regusr = r'yourmom\((.*?)\)'
        self.regusr3 = r'yourmum\((.*?)\)'
        self.regflag = r'flag\((.*?)\)'
        self.regunflag = r'flag\((.*?)\)'
        
    def Execute(self):
        try:       
            self.format_line()
            self.Comms()
            
            if ('hakcbot()' in self.msg):
                self.Hakcbot()
            elif ('commands()' in self.msg):
                self.Commands()
            elif ('youtube()' in self.msg):
                self.Youtube()
            elif ('time()' in self.msg):
                self.Time()
            elif ('github()' in self.msg):
                self.Github()
            elif ('discord()' in self.msg):
                self.Discord()      

        except Exception:
            pass   
                                               
    def Hakcbot(self):
        message = 'I will be finishing this bot later on stream'
        self.sendMessage(message)
        print('hakcbot: {}'.format(message))
                      
    def Commands(self):
        message = '<c> !playlist > music. - !discord > discord link - !github > github link - !parrot > why I use parrot - !commands > command list :D </c>'
        self.sendMessage(message)
        print('hakcbot: {}'.format(message))
 
    def Youtube(self):
        message = "Check out DOWRIGHT's YouTube here: https://www.youtube.com/channel/UCKAiTcsiD50oZvf9h0xbvCg"
        self.sendMessage(message)
        print('hakcbot: {}'.format(message))

    def Discord(self):
        message = 'Join the Discord --> https://Discord.gg/KSCHNfa'
        self.sendMessage(message)
        print('hakcbot: {}'.format(message))
        
    def Github(self):
        message = "Check out DOWRIGHT's GitHub here: https://github.com/DOWRIGHTTV/TOOLS"
        self.sendMessage(message)
        print('hakcbot: {}'.format(message))
                            
    def Time(self):
        current_time = time.localtime()
        time.strftime('%Y-%m-%d %A', current_time)
        message = "DOWRIGHT's time is {}".format(time.strftime('%H:%M:%S', current_time))
        self.sendMessage(message)
        print('hakcbot: {}'.format(message))
                           

    def Comms(self):
        try:
#            if(self.user in modList):
            if (self.user == 'dowright'):
            
                if ('unflag(' in self.msg):
                    if ('!' in self.msg or '/' in self.msg or '.' in self.msg or ' ' in self.msg):
                        pass
                    else:
                        self.arG = re.findall(self.regunflag, self.msg)[0]
                        uList.remove('{}'.format(self.arG))
                        print('Unflagged {}'.format(self.arG))
                        
                elif ('flag(' in self.msg):
                    if ('!' in self.msg or '/' in self.msg or '.' in self.msg or ' ' in self.msg):
                        pass
                    else:
                        self.arG = re.findall(self.regflag, self.msg)[0]
                        uList.append(self.arG)
                        print('Flagged {}'.format(self.arG))
            else:
                pass
            for user in uList:
                if (user == self.user):
                    message = 'lol, {} iz a nerd'.format(user)
                    self.sendMessage(message)
                    print('hakcbot: {}'.format(message))
        except Exception as E:
            print(E)

##MOMSES CODE, YOUR##                 
        if ('yourmom(' in self.msg):
            if ('!' in self.msg or '/' in self.msg or '.' in self.msg or ' ' in self.msg):
                pass
            else:    
                self.arG = re.findall(self.regusr, self.msg)[0]
                message = "{}'s mom goes to college".format(self.arG)
                self.sendMessage(message)
                print('hakcbot: {}'.format(message))

        elif ('yourmum(' in self.msg):
            if ('!' in self.msg or '/' in self.msg or '.' in self.msg or ' ' in self.msg):
                pass
            else:    
                self.arG = re.findall(self.regusr3, self.msg)[0]
                message = "{}'s mum goes to college".format(self.arG)
                self.sendMessage(message)
                print('hakcbot: {}'.format(message))

## --------------------##     
                           
    def sendMessage(self, message):
        mT = 'PRIVMSG #{} :{}'.format(CHANNEL, message)
        self.hI.s.send('{}\r\n'.format(mT).encode("utf-8"))

            
    def format_line(self):
            line = self.line.split(':', 2)
            user = line[1].split('!')
            self.user = user[0]
            self.msg = line[2]
            print('{}: {}'.format(self.user, self.msg))            
      
            
class Main:   
    def __init__(self):
#        try:
        hI = Hakcbot_Init()
        Hakcbot_Run(hI)
#        except KeyboardInterrupt as LOL:
#            print('-' * 32)  
#            print('Exiting the coolest bot ever. :(') 
#            print('-' * 32)       
Main()



