#!/usr/bin/python3

import re

class Spam:
    def __init__(self, Hakcbot):
        self.Hakcbot = Hakcbot
        self.urlregex = re.compile(
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # Domain
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # IP Address
        r'(?::\d+)?' # Optional Port eg :8080
        r'(?:/?|[/?]\S+)', re.IGNORECASE) # Sepcific pages in url eg /homepage
        

        
#        self.regusr = r'yourmom\((.*?)\)'
#        self.regusr3 = r'yourmum\((.*?)\)'
#        self.regflag = r'flag\((.*?)\)'
#        self.regunflag = r'flag\((.*?)\)'
        
    
    def Main(self, line):
        self.line = line
        try:
            self.format_line()
            self.urlFilter()
        except Exception:
            pass                
        
    def urlFilter(self):       
        urlmatch = re.findall(self.urlregex, self.msg)
        if urlmatch:
            print('would time out')
            return True
        else:
            pass

    def format_line(self):
        try:
            line = self.line.split(':', 2)
            user = line[1].split('!')
            self.user = user[0]
            self.msg = line[2]
        except Exception:
            raise Exception('Format Line Error')
