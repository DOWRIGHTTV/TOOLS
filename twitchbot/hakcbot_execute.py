#!/usr/bin/python3


import re
import threading
from config import *
import time
import requests
import json

uList = []

class Execute:
    def __init__(self, Hakcbot):
        self.Hakcbot = Hakcbot
        self.regusr = re.compile(r'yourmom\((.*?)\)')
        self.regusr3 = re.compile(r'yourmum\((.*?)\)')
        self.regflag = re.compile(r'flag\((.*?)\)')
        self.regunflag = re.compile(r'flag\((.*?)\)')
        self.regpraise = re.compile(r'praise\((.*?)\)')
        
        self.msgreg = re.compile(r'user-type=(.*)')
        
        self.hakcinfo = True
        self.hakccommands = True
        self.hakcyoutube = True
        self.hakcdiscord = True
        self.hakcgithub = True
        self.hakcsub = True
        self.hakcuptime = True
        self.hakctime = True
        self.hakcplaylist = True
        self.hakcparrot = True   
        self.hakcpraise = True             
        self.hakcyourmom = True
        self.hakcyourmum = True
        
        with open('commands.json', 'r') as cmds:
            self.commands = json.load(cmds)
                
    def Main(self, line):
        self.line = line
        command = None
        try:     
            self.format_line()
            try:
                command, CD = self.Comms()
            except Exception:
                pass
            
            commands = {'Commands', 'Youtube', 'Discord', 'Github',
                        'Sub', 'Uptime', 'Time', 'Playlist', 'Parrot'}
            
            msg = self.msg.split(' ')
            go = False
            for word in msg:
                if (go != True):
                    for cmd in commands:
                        if '{}()'.format(cmd).lower() == word.lower().strip('\r') \
                        and getattr(self, 'hakc{}'.format(cmd).lower()):
                                if '{}()'.format(cmd).lower() == 'uptime()':
                                    threading.Thread(target=self.Uptime, args=(cmd,)).start()
                                else:
                                    command, CD = self.Command(cmd)
                                go = True
                           
            if (command):
                threading.Thread(target=self.Cooldown, args=(command, CD)).start()
            else:
                pass           
        except Exception as E:
            print(E)
            
    def Command(self, cmd):
        name = self.commands[cmd]['CD Name'] 
        CD = self.commands[cmd]['CD Time']           
        if (cmd == 'Time'):
            message = self.commands[cmd]['message']
            current_time = time.localtime()
            ltime = time.strftime('%H:%M:%S', current_time)
            message = '{} {}'.format(message, ltime)
            print('hakcbot: {}'.format(message))
            self.sendMessage(message)
            return(name, CD)
        else:
            message = self.commands[cmd]['message']
            print('hakcbot: {}'.format(message))
            self.sendMessage(message)
            return(name, CD)

    def Uptime(self, cmd):
        uptime = requests.get("https://decapi.me/twitch/uptime?channel=dowright")
        uptime = uptime.text.strip('\n')
        message = self.commands[cmd]['message']
        message = '{} {}'.format(message, uptime)
        print('hakcbot: {}'.format(message))
        self.sendMessage(message)
        self.Cooldown(self.commands[cmd]['CD Name'], self.commands[cmd]['CD Time'])   
                    
    def Comms(self):
#        if(self.user in modList):
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
                
        if ('praise(' in self.msg and self.hakcpraise == True):
            if ('!' in self.msg or '/' in self.msg or '.' in self.msg or ' ' in self.msg):
                pass
            else:    
                self.arG = re.findall(self.regpraise, self.msg)[0]
                if (self.arG == 'thesun'):
                    message = "\ [T] /"
                    self.sendMessage(message)
                else:
                    message = 'Can only praise the sun.'
                    self.sendMessage(message)
                print('hakcbot: {}'.format(message))
                return('hakcpraise', 30)
              
        elif ('yourmom(' in self.msg and self.hakcyourmom == True):
            if ('!' in self.msg or '/' in self.msg or '.' in self.msg or ' ' in self.msg):
                pass
            else:    
                self.arG = re.findall(self.regusr, self.msg)[0]
                message = "{}'s mom goes to college".format(self.arG)
                self.sendMessage(message)
                print('hakcbot: {}'.format(message))
                return('hakcyourmom', 360)

        elif ('yourmum(' in self.msg and self.hakcyourmum == True):
            if ('!' in self.msg or '/' in self.msg or '.' in self.msg or ' ' in self.msg):
                pass
            else:    
                self.arG = re.findall(self.regusr3, self.msg)[0]
                message = "{}'s mum goes to college".format(self.arG)
                self.sendMessage(message)
                print('hakcbot: {}'.format(message))
                return('hakcyourmum', 360)  
                           
    def sendMessage(self, message):
        mT = 'PRIVMSG #{} :{}'.format(CHANNEL, message)
        self.Hakcbot.s.send('{}\r\n'.format(mT).encode("utf-8"))
        
    def format_line(self):
        try:
            msg = re.findall(self.msgreg, self.line)[0]
            msg = msg.split(':', 2)
            user = msg[1].split('!')
            self.user = user[0]
            self.msg = msg[2]
            print('{}: {}'.format(self.user, self.msg))
        except Exception:
            raise Exception('Format Line Error')

    def Cooldown(self, command, CD):
        print('Putting {} on cooldown'.format(command))
        setattr(self, command, False)
        time.sleep(CD)
        print("Removing {}'s cooldown".format(command))
        setattr(self, command, True)
