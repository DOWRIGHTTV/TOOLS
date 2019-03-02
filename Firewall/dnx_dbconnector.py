#!/usr/bin/python3

import sqlite3
import os
import time
import datetime

class SQLConnector:
    def __init__(self):
        self.db = 'dnxfwallproxy.db'
        self.table = 'PROXYBLOCKS'
        
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()
        
        if not os.path.isfile (self.db):
            with open(self.db, 'w+') as db:
                pass
        self.c.execute('create table if not exists {} (URL, Category, Count, LastHit)'.format(self.table))
    
    def Disconnect(self):
        try:
            self.conn.close()
        except Exception as E:
            print(E)
        
    def Input(self, url, cat, timestamp, db='PROXYBLOCKS'):
        results = self.EntryCheck(url)
        print('INPUT RESULTS: {}'.format(results))
        if not results:
            self.c.execute('insert into {} values (?, ?, ?, ?)'.format(db), (url, cat, 1, timestamp))
        else:
            i = results[0][2]
            i += 1
            self.c.execute('update {} set Count=?, LastHit=? where URL=?'.format(db), (i, timestamp, url))
        self.conn.commit()
                
    def EntryCheck(self, url, db='PROXYBLOCKS'):
        self.c.execute('select * from {} where URL=?'.format(db), (url,))
        results = self.c.fetchall()
        return results
        
    def QueryTOP10(self, db='PROXYBLOCKS'):
        self.c.execute('select * from {} order by LastHit desc limit 10'.format(db))
        results = self.c.fetchall()
        return results
        
    def Cleaner(self, db='PROXYBLOCKS'):
        timestamp = int(time.time())
        month = 3600*24*30       
        expire = timestamp - month                
        try:
#            self.c.execute('select * from {} where LastHit < {}'.format(db, expire))
#            LOL = self.c.fetchall()
#            print(LOL)
            self.c.execute('delete from {} where LastHit < {}'.format(db, expire))
            self.conn.commit()
        except Exception as E:
            print(E)

if __name__ == '__main__':
#    url = 'fbob.com'
    while True:
        timestamp = int(time.time())
#        timestamp = 11
        SQLC = SQLConnector()
        cat = 'douchey'
        url = input('list test url:' )
        if url == 'top10':
            results = SQLC.QueryTOP10()
            for result in results:            
                print(result[0],result[1],result[2],result[3],)
        elif url == 'clean':
            SQLC.Cleaner()       
        else:
            SQLC.Input(url, cat, timestamp)


