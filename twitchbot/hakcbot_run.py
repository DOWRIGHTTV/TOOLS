#!/usr/bin/python3


from config import *
import hakcbot_init as hakc
import re
import sched, time

import threading
import multiprocessing
import asyncio
import time

uList = []

hakcbot = hakc.Hakcbot()
hakcbot.Connect()

class Hakcbot_Run:
    def __init__(self):
        self.hakcbotExecute = Hakcbot_Execute()
        self.hakcbotAutomate = Hakcbot_Automate()
        self.hakcbotSpam = Hakcbot_Spam()

        
    def Processes(self):
        p1 = multiprocessing.Process(target=self.Hakc)
        p2 = multiprocessing.Process(target=self.Hakc2)
        
        p1.start()
        p2.start()

            
    def Hakc(self):
        rb = ''
        while True:
            rb = rb + hakcbot.s.recv(1024).decode()
            chat = rb.split('\n') 
            rb = chat.pop()
                    
            for line in chat:
                if ('PING :tmi.twitch.tv' == line):                    
                    print(line)
                    hakcbot.s.send('PONG :tmi.twitch.tv\r\n'.encode("utf-8"))
                else:
                    spam = self.hakcbotSpam.Main(line)
                    if (not spam):
                        self.hakcbotExecute.Main(line)

    
    def Hakc2(self):
        key = ['Commands', 'Discord', 'Github']
        value = [50, 45, 30]
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(asyncio.gather(self.hakcbotAutomate.Timers(key[0], value[0]), self.hakcbotAutomate.Timers(key[1], value[1]), self.hakcbotAutomate.Timers(key[2], value[2])))
            
        except Exception as E:
            print(E)
            
class Hakcbot_Automate:
    def __init__(self):
        self.hakcbotExecute = Hakcbot_Execute()
                
    async def Timers(self, key, value):
        #Commands#
        try:
            while True:
                await asyncio.sleep(60 * value)
                eval('self.hakcbotExecute.{}()'.format(key))

        except Exception as E:
            print(E)


class Hakcbot_Execute:
    def __init__(self):
        self.regusr = r'yourmom\((.*?)\)'
        self.regusr3 = r'yourmum\((.*?)\)'
        self.regflag = r'flag\((.*?)\)'
        self.regunflag = r'flag\((.*?)\)'
        
        self.hakcinfo = True
        self.hakccommands = True
        self.hakcyoutube = True
        self.hakctime = True
        self.hakcgithub = True
        self.hakcdiscord = True
        self.hakcyourmom = True
        self.hakcyourmum = True
                
    def Main(self, line):
        self.line = line
        try:
            command = None       
            self.format_line()
            command = self.Comms()
            
            if ('hakcbot()' in self.msg and self.hakcinfo == True):
                command, CD = self.HakcbotInfo()
            elif ('commands()' in self.msg and self.hakccommands == True):
                command, CD = self.Commands()
            elif ('youtube()' in self.msg and self.hakcyoutube == True):
                command, CD = self.Youtube()
            elif ('discord()' in self.msg and self.hakcdiscord == True):
                command, CD = self.Discord() 
            elif ('github()' in self.msg and self.hakcgithub == True):
               command, CD =  self.Github()
            elif ('time()' in self.msg and self.hakctime == True):
               command, CD =  self.Time()
            
            if (command):         
                threading.Thread(target=self.Cooldown, args=(command, CD)).start()
            else:
                pass
        except Exception as E:
            print(E)
                                               
    def HakcbotInfo(self):
        message = 'I will be finishing this bot later on stream'
        self.sendMessage(message)
        print('hakcbot: {}'.format(message))
        return('hakcinfo', 180)
                      
    def Commands(self):
        message = '<c> !playlist > music. - !discord > discord link - !github > github link - !parrot > why I use parrot - !commands > command list :D </c>'
        self.sendMessage(message)
        print('hakcbot: {}'.format(message))
        return('hakccommands', 180)
    
    def Youtube(self):
        message = "Check out DOWRIGHT's YouTube here: https://www.youtube.com/channel/UCKAiTcsiD50oZvf9h0xbvCg"
        self.sendMessage(message)
        print('hakcbot: {}'.format(message))
        return('hakcyoutube', 180)
        
    def Discord(self):
        message = 'Join the Discord --> https://Discord.gg/KSCHNfa'
        self.sendMessage(message)
        print('hakcbot: {}'.format(message))
        return('hakcdiscord', 180)
        
    def Github(self):
        message = "Check out DOWRIGHT's GitHub here: https://github.com/DOWRIGHTTV/TOOLS"
        self.sendMessage(message)
        print('hakcbot: {}'.format(message))
        return('hakcgithub', 180)
                            
    def Time(self):
        current_time = time.localtime()
        time.strftime('%Y-%m-%d %A', current_time)
        message = "DOWRIGHT's time is {}".format(time.strftime('%H:%M:%S', current_time))
        self.sendMessage(message)
        print('hakcbot: {}'.format(message))
        return('hakctime', 300)

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
        if ('yourmom(' in self.msg and self.hakcyourmom == True):
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
                
## --------------------##     
                           
    def sendMessage(self, message):
        mT = 'PRIVMSG #{} :{}'.format(CHANNEL, message)
        hakcbot.s.send('{}\r\n'.format(mT).encode("utf-8"))

            
    def format_line(self):
            line = self.line.split(':', 2)
            user = line[1].split('!')
            self.user = user[0]
            self.msg = line[2]
            print('{}: {}'.format(self.user, self.msg))

    def Cooldown(self, command, CD):
        print('Putting {} on cooldown'.format(command))
        setattr(self, command, False)
        time.sleep(CD)
        print("Removing {}'s cooldown".format(command))
        setattr(self, command, True)


class Hakcbot_Spam:
    def __init__(self):
#        self.regusr = r'yourmom\((.*?)\)'
#        self.regusr3 = r'yourmum\((.*?)\)'
#        self.regflag = r'flag\((.*?)\)'
#        self.regunflag = r'flag\((.*?)\)'
        
        self.domainsList = ['.com', '.net', '.ru']
    
    def Main(self, line):
        for tld in self.domainsList:
            if tld in line:
                print('would time out')
                return True
            else:
                continue
        
        


            
class Main:
    def __init__(self):
#        try:
        hakcbotRun = Hakcbot_Run()
        hakcbotRun.Processes()
#        except KeyboardInterrupt as LOL:
#            print('-' * 32)  
#            print('Exiting the coolest bot ever. :(') 
#            print('-' * 32)       
Main()



