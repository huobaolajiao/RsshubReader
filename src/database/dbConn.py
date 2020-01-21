# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 08:56:33 2020

@author: wangyouqish
"""
import sqlite3
import os

def getConn():
    os.chdir(os.path.join(os.path.abspath(".."),'database'))
    if(os.path.isfile("info.db")):
        conn = sqlite3.connect('info.db',check_same_thread = False)
    else:
        conn = sqlite3.connect('info.db',check_same_thread = False)
        conn.execute('''CREATE TABLE [rssData](
        [rssName] TEXT, 
        [title] TEXT UNIQUE, 
        [summary] TEXT, 
        [timestamp] INT, 
        [link] TEXT, 
        [downloaded] BOOL DEFAULT 0);''')
        
        conn.execute('''CREATE TABLE [normalrsslinks](
        [link] TEXT NOT NULL, 
        [name] TEXT NOT NULL UNIQUE, 
        [round] INT, 
        [lastget] INT DEFAULT 0, 
        [active] BOOL DEFAULT 1, 
        [title] TEXT, 
        [unread] INT DEFAULT 0);''')
        conn.execute('''CREATE TABLE [rsshubtasks](
        [active] BOOL DEFAULT 1, 
        [router] TEXT NOT NULL, 
        [name] TEXT NOT NULL UNIQUE, 
        [round] INT, 
        [lastget] INT DEFAULT 0, 
        [recommendedServerID] INT DEFAULT 0, 
        [autoDownload] BOOL DEFAULT 0, 
        [title] TEXT, 
        [unread] INT DEFAULT 0);''')
        conn.execute('''CREATE TABLE [rsshubServers](
        [ID] INT, 
        [Adress] TEXT, 
        [FuncNum] INT, 
        [FirstCheck] DATE, 
        [LastCheck] DATE);''')
        conn.execute("INSERT INTO rsshubServers( ID, Adress, FuncNum, FirstCheck, LastCheck) VALUES(1, 'https://rsshub.app', 1019, '2020-01-01', '2020-01-21')")
        conn.execute("INSERT INTO rsshubServers( ID, Adress, FuncNum, FirstCheck, LastCheck) VALUES(2, 'https://uneasy.win/rss', 1000, '2020-01-01', '2020-01-21')")
        conn.commit()
    
    return conn