# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 20:37:17 2020

@author: wangyouqish
"""

import sys
sys.path.append("..")
import os
print(os.getcwd())
import time
import database.dbConn as dbConn
import log.logCenter as logCenter
import autoDownloader.downloadDouyinVideo as downloadDouyinVideo
import spider.rssSpider as rssSpider
import spider.rsshubServers as rsshubServers


while(1):
    try:
        rssSpider.getAllRssData()
        downloadDouyinVideo.downloadAllVideo()
        time.sleep(60)
    except:
        print("execute error")

        
