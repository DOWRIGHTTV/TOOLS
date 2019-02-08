#!/usr/bin/python3

import re
import time
import threading
from config import CHANNEL

class Spam:
    def __init__(self, Hakcbot):
        self.Hakcbot = Hakcbot
        self.tlddict = {}
        self.permitlist = []
        
        self.regulars = ['bitnomadlive']
        self.whitelist = {'pastebin.com', 'twitch.tv', 'github.com'} # PEP 8 IS BULLSHIT......FAIL
        
        self.permituser = re.compile(r'permit\((.*?)\)')
        self.urlregex = re.compile(
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z]{2,}\.?)|' # Domain
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # IP Address
        r'(?::\d+)?' # Optional Port eg :8080
        r'(?:/?|[/?]\S+)', re.IGNORECASE) # Sepcific pages in url eg /homepage
        
        self.tagsreg = re.compile(r'@badges=(.*?)user-type=')
        self.msgreg = re.compile(r'user-type=(.*)')
    
    def Main(self, line):
        self.line = line
        try:
            self.format_line()
            self.HakcbotPermit()
            spam = self.urlFilter()
            return(spam)
        except Exception as E:
            print(E)                
      
    def urlFilter(self):
        urlcheck = {}
#        print(self.msg)
        urlmatch = re.findall(self.urlregex, self.msg)
        if urlmatch:
#            print('{} : {}'.format(self.user, self.subscriber))
            if (self.user in self.regulars or self.subscriber == 'subscriber=1' \
            or self.user in self.permitlist):
                pass
            else:            
                for url in self.whitelist:
                    if url in self.msg:
                        urlcheck.add(True)
                if (True not in urlcheck):
                    print('BLOCKED || {} : {}'.format(self.user, urlmatch[0]))
                    message = '/timeout {} {} {}'.format(self.user, 10, urlmatch[0])
                    response = '{}, ask for permission to post links.'.format(self.user)
                    self.sendMessage(message, response)
                    return True

    def HakcbotPermit(self):
#        if(self.user in modList):
        if (self.user == 'dowright'):
            if ('permit(' in self.msg):
                if ('!' in self.msg or '/' in self.msg or '.' in self.msg or ' ' in self.msg):
                    pass
                else:
                    user = re.findall(self.permituser, self.msg)[0]
                    threading.Thread(target=self.HakcbotPermitThread, args=(user,)).start()
                    message = '/untimeout {}'.format(self.user)
                    response = '{} can post links for 3 minutes.'.format(user)
                    self.sendMessage(message, response)
                         
    def HakcbotPermitThread(self, user):
        self.permitlist.append(user)
        time.sleep(60 * 3)
        self.permitlist.remove(user)

    def format_line(self):
        try:
            tags = re.findall(self.tagsreg, self.line)[0]
            msg = re.findall(self.msgreg, self.line)[0]
            msg = msg.split(':', 2)
            tags = tags.split(';')
            user = msg[1].split('!')
            self.user = user[0]
            self.msg = msg[2]
            self.subscriber = tags[8]
            if ('subscriber' in self.subscriber):
                pass
            else:
                self.subscriber = tags[9]        
        except Exception:
            raise Exception('Spam Format Line Error')            
    def sendMessage(self, message, response=None):
        mT = 'PRIVMSG #{} :{}'.format(CHANNEL, message)
        self.Hakcbot.s.send('{}\r\n'.format(mT).encode("utf-8"))
        if (not response):
            pass
        else:
            rT = 'PRIVMSG #{} :{}'.format(CHANNEL, response)
            self.Hakcbot.s.send('{}\r\n'.format(rT).encode("utf-8"))
                
            
        
        
        
