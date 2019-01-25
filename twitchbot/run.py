#!/usr/bin/python3

from socket import *
from config import *
import re

import time


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
        
        self.Hakc()
        
    def Hakc(self):
        rb = ''
        while True:
            rb = rb + self.hI.s.recv(1024).decode()
            chat = rb.split('\n') 
            rb = chat.pop()
                     
            for line in chat:
                if ('PING :tmi.twitch.tv' in line):
                    print(line)
                    self.hI.s.send('PONG :tmi.twitch.tv\r\n'.encode("utf-8"))
                else:
                    Hakcbot_Execute(self.hI, line)
                

class Hakcbot_Execute:
    def __init__(self, hI, line):
        self.line = line
        self.hI = hI
        self.regusr = r'yourmom\((.*?)\)'
        try:        
            self.format_line()       
            
            if ('hakcbot()' in self.msg):
                message = 'I will be finishing this bot later on stream'
                self.sendMessage(message)
                print('hakcbot: {}'.format(message))
                
            elif ('yourmom(' in self.msg):
                self.arG = re.findall(self.regusr, self.msg)[0]
                message = "{}'s mom goes to college".format(self.arG)
                self.sendMessage(message)
                print('hakcbot: {}'.format(message))
            
            elif ('commands()' in self.msg):
                message = '<c> !playlist > music. - !discord > discord link - !github > github link - !parrot > why I use parrot - !commands > command list :D </c>'
                self.sendMessage(message)
                print('hakcbot: {}'.format(message))
                
            elif ('time()' in self.msg):
                current_time = time.localtime()
                time.strftime('%Y-%m-%d %A', current_time)
                message = "DOWRIGHT's time is {}".format(time.strftime('%H:%M:%S', current_time))
                self.sendMessage(message)
                print('hakcbot: {}'.format(message))
                
        except Exception:
            pass
                            
                        
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
        hI = Hakcbot_Init()
        Hakcbot_Run(hI)
        
Main()



