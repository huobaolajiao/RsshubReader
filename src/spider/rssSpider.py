# -*- coding: utf-8 -*-
"""
@author: wangyouqish
"""
import sys
sys.path.append("..")
import time,datetime
import pytz
import requests
import feedparser
import threading
import database.dbConn as dbConn
import log.logCenter as logCenter


def getFeedFromLink(url,name):
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
    try:
        page = requests.get(url, headers=head,timeout=(10,10))
        page.encoding = 'utf-8'
        page_content = page.text
        if(page.status_code==404 or page.status_code==403):
            logger.error(name+" 404/403 failed "+url)
            return None
    except:
        logger.error(name+" download failed "+url)
        return None
    rss = feedparser.parse(page_content)
    return rss

def getRsshubFeed(router,name,recommendedServerID):
    downloadedFlag=0
    conn=dbConn.getConn()
    cSer = conn.cursor()
    cursorSer = cSer.execute("SELECT ID,Adress,FuncNum,FirstCheck,LastCheck from rsshubServers where ID={}".format(recommendedServerID))
    rss=None
    if(recommendedServerID!=0):
        for row in cursorSer:
            server=row[1]
            url=server+router
            rss = getFeedFromLink(url,name)
            if(rss!=None):
                downloadedFlag=1
    cursorSer = cSer.execute("SELECT ID,Adress,FuncNum,FirstCheck,LastCheck from rsshubServers")#用所有服务器遍历
    for row in cursorSer:
        if(downloadedFlag==0):
            server=row[1]
            url=server+router
            rss = getFeedFromLink(url,name)
            if(rss!=None):
                downloadedFlag=1
    conn.close()
    return rss
def saveOneNormalRss(url,name,unread):
    conn=dbConn.getConn()
    old=0
    new=0
    rss = getFeedFromLink(url,name)
    if(rss==None):
        return
    for post in rss.entries:
        title=post.title
        summary=post.summary
        link=post.link
        try:
            itemTimestamp=int(time.mktime(post.published_parsed))#第一类time是每一条新闻有发布时间，被feedparser捕获
        except:
            try:
                gmtTime=rss.feed.updated#第二类time是GMT时间，从xml文件生成时间获取
                local_tz = pytz.timezone('Asia/Shanghai')
                utcDT=datetime.datetime.strptime(gmtTime,"%a, %d %b %Y %H:%M:%S GMT")
                itemTimestamp=int(time.mktime(utcDT.replace(tzinfo=pytz.utc).astimezone(local_tz).timetuple()))
            except:  
                try:
                    bjTime=post.published
                    bjT=time.strptime(bjTime,"%a,%d %b %Y %H:%M:%S +0800")
                    itemTimestamp=int(time.mktime(bjT))#仅为了适配cili001的时间格式
                except:
                    itemTimestamp=int(time.time())
        try:
            conn.execute("INSERT INTO rssData (rssName,title,summary,timestamp,link) VALUES ('{}','{}','{}',{},'{}')".format(name,title,summary,itemTimestamp,link))
            new=new+1
        except:
            old=old+1 #增加新闻失败就是老的新闻   
    try:
        unread=unread+new
        sqlupdate="UPDATE normalrsslinks set lastget ={} ,unread={} where name='{}'".format(str(int(time.time())),unread,name)#更新rss任务列表最后提交时间
        conn.execute(sqlupdate)
        conn.commit()
        conn.close()
    except:
        logger.warning("sqlerror   "+name)
    logger.info(name+"  add new:"+str(new)+"  old:"+str(old))


def saveOneRsshub(router,name,recommendedServerID,unread):
    conn=dbConn.getConn()
    old=0
    new=0   
    rss = getRsshubFeed(router,name,recommendedServerID)
    
    if(rss==None):
        logger.warning(name+" all download failed "+router)#全部下载失败，可能是网络不好或者router无效、故障
        return
    for post in rss.entries:
        title=post.title
        summary=post.summary
        link=post.link
        try:
            itemTimestamp=int(time.mktime(post.published_parsed))
        except:
            try:
                gmtTime=rss.feed.updated
                local_tz = pytz.timezone('Asia/Shanghai')
                utcDT=datetime.datetime.strptime(gmtTime,"%a, %d %b %Y %H:%M:%S GMT")
                itemTimestamp=int(time.mktime(utcDT.replace(tzinfo=pytz.utc).astimezone(local_tz).timetuple()))
            except:  
                itemTimestamp=int(time.time())
        try:
            conn.execute("INSERT INTO rssData (rssName,title,summary,timestamp,link) VALUES ('{}','{}','{}',{},'{}')".format(name,title,summary,itemTimestamp,link))
            new=new+1
        except:
            old=old+1    
    try:
        unread=unread+new
        sqlupdate="UPDATE rsshubtasks set lastget ={} ,unread={}  where name='{}'".format(str(int(time.time())),unread,name)
        conn.execute(sqlupdate)
        conn.commit()
        conn.close()
    except:
        logger.warning("sqlerror   "+name)
    logger.info("rsshubtask "+name+" add new:"+str(new)+"  old:"+str(old))

def updateAllTasksTitle():
    conn=dbConn.getConn()
    cTask = conn.cursor()
    cursor = cTask.execute("SELECT link , name , round , lastget ,title from normalrsslinks where active=1")
    for row in cursor:
        rss=getFeedFromLink(row[0],row[1])
        conn.execute("UPDATE normalrsslinks set title='{}' where name='{}'".format(rss.feed.title,row[1]))
    cursor = cTask.execute("SELECT router , name , round , lastget , recommendedServerID, title from rsshubtasks where active=1")
    for row in cursor:
        rss=getRsshubFeed(row[0],row[1],row[4])
        conn.execute("UPDATE rsshubtasks set title='{}' where name='{}'".format(rss.feed.title,row[1]))
    conn.commit()
    conn.close()    

def getAllRssData():
    conn=dbConn.getConn()
    taskDoCount=0
    taskWaitCount=0
    conn=dbConn.getConn()
    cTask = conn.cursor()
    cursor = cTask.execute("SELECT link , name , round , lastget ,unread from normalrsslinks where active=1")
    thread_list = []
    for row in cursor:
        if((int(time.time())-int(row[3]))>row[2]):
            t= threading.Thread(target=saveOneNormalRss,args=(row[0],row[1],row[4]))
            t.start()            
            logger.debug(row[1]+" "+row[0]+" start")
            taskDoCount=taskDoCount+1
            thread_list.append(t)
        else:
            logger.debug(row[1]+"  less than round")
            taskWaitCount=taskWaitCount+1
    #以上为常规rss任务
    cursor = cTask.execute("SELECT router , name , round , lastget , recommendedServerID ,unread from rsshubtasks where active=1")
    for row in cursor:
        if((int(time.time())-int(row[3]))>row[2]):
            t= threading.Thread(target=saveOneRsshub,args=(row[0],row[1],row[4],row[5]))
            t.start()         
            logger.debug("rsshub "+row[1]+" "+row[0]+" start")
            taskDoCount=taskDoCount+1
            thread_list.append(t)
        else:
            logger.debug("rsshub "+row[1]+"  less than round")
            taskWaitCount=taskWaitCount+1
    for t in thread_list:
        t.join() 
    logger.info(str(taskDoCount)+" tasks done "+str(taskWaitCount)+" tasks wait")
    conn.commit()
    conn.close()
    #以上为rsshub的router任务

    

#以下main开始，被import的初始化在if  main外
logger=logCenter.getLogger("rssSpider")
if __name__ == "__main__":
    getAllRssData()
    