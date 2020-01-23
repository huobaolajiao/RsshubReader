# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 23:02:41 2020

@author: wangyouqish
"""
import sys
sys.path.append("..")
import requests
import time
import threading
import os
import database.dbConn as dbConn
import log.logCenter as logCenter
from urllib.parse import quote

def downloadOneVideo(name,title,url,timestamp):
    conn=dbConn.getConn()
    global VideoCount
    try:
        os.chdir(os.path.join(os.path.abspath('..'),'web','static'))
        head = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'}
        page = requests.get(url.replace("/playwm/","/play/"), headers=head)
        page.encoding = 'utf-8'
        #print(page.url)
        webvideopage = requests.get(page.url,headers=head)
        if(os.path.exists(os.path.join("video",name))==0):
            os.makedirs(os.path.join("video",name))
        with open(os.path.join("video",name,title+"_"+str(timestamp)+".mp4"), "wb") as code:
            code.write(webvideopage.content)
        summary='''<p style="display:block; text-align:center;">
        <video controls="controls" width="300" height="600" src="/video/{}/{}">
        </video></p>'''.format(name,quote(title)+"_"+str(timestamp)+".mp4")
        conn.execute("UPDATE rssData set downloaded = 1,summary='{}'  where rssName='{}' and title='{}'".format(summary,name,title))
        conn.commit()
        VideoCount=VideoCount+1
        logger.info(name+" "+url+" downloaded")
    except:
        pass
    conn.close()
      
        
def downloadAllVideo():
    conn=dbConn.getConn()
    global VideoCount
    VideoCount=0
    routerCount=0
    cTask = conn.cursor()#大的任务表
    cData = conn.cursor()#每个data_表
    thread_list = []
    cursor = cTask.execute("SELECT name ,router,autoDownload from rsshubtasks")
    for row in cursor:
        if(row[1].find("douyin")>=0 and row[2]==1):
            routerCount=routerCount+1
            cursor2=cData.execute("SELECT title,link,downloaded,timestamp from rssData where rssName='{}'".format(row[0]))
            for row2 in cursor2:
                if(row2[2]==0):
                    t= threading.Thread(target=downloadOneVideo,args=(row[0],row2[0],row2[1],row2[3]))
                    t.start()            
                    thread_list.append(t)
        
    for t in thread_list:
        t.join() 
    logger.info(str(routerCount)+" routers need autoDownload "+str(VideoCount)+" videos downloaded")
    conn.close()


#以下为main开始
VideoCount=0
logger=logCenter.getLogger("dyDownload")
conn=dbConn.getConn()
if __name__ == "__main__":
    downloadAllVideo()
    logCenter.destroyLogger(logger)
        
