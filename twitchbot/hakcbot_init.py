#!/usr/bin/python3

from socket import *
from config import *

class Hakcbot:
    def __init__(self):
        self.s = socket()
        
    def Connect(self):
        self.openSocket()
        self.joinRoom()
        
    
    def openSocket(self):
        self.s.connect((HOST, PORT))
        self.s.send('PASS {}\r\n'.format(PASS).encode("utf-8"))
        self.s.send('NICK {}\r\n'.format(IDENT).encode("utf-8"))
        self.s.send('JOIN #{}\r\n'.format(CHANNEL).encode("utf-8"))
        self.s.send('CAP REQ :twitch.tv/tags\r\n'.encode("utf-8"))
        
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
 
