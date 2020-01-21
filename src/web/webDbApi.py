import sys
sys.path.append("..")
import database.dbConn as dbConn
import spider.rssSpider as rssSpider
def dict_factory(cursor, row):
    d = {}
    for index, col in enumerate(cursor.description):
        d[col[0]] = row[index]
    return d
def countOneRecords(rssName):
    conn=dbConn.getConn()
    cursor=conn.execute("select count(rowid) from rssData where rssName='{}'".format(rssName))
    for row in cursor:
        cnt=row[0]
    conn.close()
    return cnt
def countAllRecords():
    conn=dbConn.getConn()
    cursor=conn.execute("select count(rowid) from rssData")
    for row in cursor:
        cnt=row[0]
    conn.close()
    return cnt

def addNormalRssLink(url,name,round,title):
    if(url=="" or name=="" or round<=0):
        return -1
    conn=dbConn.getConn()
    try:
        linksql="INSERT INTO normalrsslinks (link , name , round , title) VALUES ('{}','{}',{},'{}')".format(url,name,round,title)
        conn.execute(linksql)#建普通rss任务
        conn.commit()
        conn.close()
    except:
        return -1
    return 0
def addRsshubTask(router,name,round,recommendedServerID,title):
    if(router=="" or name=="" or round<=0 or recommendedServerID<0):
        return -1
    conn=dbConn.getConn()
    try:
        linksql="INSERT INTO rsshubtasks (router , name , round ,recommendedServerID,title) VALUES ('{}','{}',{},{},'{}')".format(router,name,round,recommendedServerID,title)
        #建rsshub任务
        conn.execute(linksql)
        conn.commit()
        conn.close()
    except:
        return -1
    return 0

def updateNormalRssLink(url,name,round,title):
    if(url=="" or name=="" or round<=0):
        return -1
    conn=dbConn.getConn()
    try:
        linksql="UPDATE normalrsslinks set link='{}' , round={} ,title='{}'  where name='{}' ".format(url,round,title,name)
        conn.execute(linksql)#修改普通rss任务
        conn.commit()
        conn.close()
    except:
        return -1
    return 0
def updateRsshubTask(router,name,round,recommendedServerID,title):
    if(router=="" or name=="" or round<=0 or recommendedServerID<0):
        return -1
    conn=dbConn.getConn()
    try:
        linksql="UPDATE rsshubtasks set router='{}' , round={} ,recommendedServerID={},title='{}' where name='{}'".format(router,round,recommendedServerID,title,name)
        #修改rsshub任务
        conn.execute(linksql)
        conn.commit()
        conn.close()
    except:
        return -1
    return 0
def getRssTasks():
    normalDict=[]
    rsshubDict=[]
    conn=dbConn.getConn()
    cTask = conn.cursor()
    cursor = cTask.execute("SELECT link , name , round , lastget, title,unread from normalrsslinks where active=1")
    for row in cursor:
        d =dict_factory(cursor,row)
        normalDict.append(d)
    cursor = cTask.execute("SELECT router , name , round , lastget , recommendedServerID ,title ,unread from rsshubtasks where active=1")
    for row in cursor:
        d =dict_factory(cursor,row)
        rsshubDict.append(d)
    conn.close()
    return (normalDict,rsshubDict)

def getRssTaskInfo(rssName):
    conn=dbConn.getConn()
    cTask = conn.cursor()
    cursor = cTask.execute("SELECT link , name , round , lastget, title,unread from normalrsslinks where name='{}'".format(rssName))
    for row in cursor:
        newDict =dict_factory(cursor,row)
        newDict['isRsshub']=0
    cursor = cTask.execute("SELECT router , name , round , lastget , recommendedServerID ,title ,unread from rsshubtasks where name='{}'".format(rssName))
    for row in cursor:
        newDict =dict_factory(cursor,row)
        newDict['isRsshub']=1
    conn.close()
    return newDict
def getAllDbRssData(start=0,num=10):
    rssDict=[]
    conn=dbConn.getConn()
    c= conn.cursor()
    cursor = c.execute("SELECT rssName,title,summary,timestamp,link,downloaded from rssData order by timestamp desc limit {},{}".format(start,num))
    for row in cursor:
        d =dict_factory(cursor,row)
        rssDict.append(d)
    conn.close()
    return rssDict

def getOneDbRssData(name,start=0,num=10):
    rssDict=[]
    conn=dbConn.getConn()
    c= conn.cursor()
    cursor = c.execute("SELECT rssName,title,summary,timestamp,link,downloaded from rssData where rssName='{}' order by timestamp desc limit {},{}".format(name,start,num))
    for row in cursor:
        d =dict_factory(cursor,row)
        rssDict.append(d)
    if(rssDict!=[]):
        conn.execute("UPDATE normalrsslinks set unread=0 where name='{}'".format(row[0]))
        conn.execute("UPDATE rsshubtasks set unread=0 where name='{}'".format(row[0]))
        conn.commit()
    conn.close()
    return rssDict

def deleteRssTask(rssName):
    conn=dbConn.getConn()
    conn.execute("DELETE FROM normalrsslinks  where name='{}'".format(rssName))
    conn.execute("DELETE FROM rsshubtasks where name='{}'".format(rssName))
    conn.execute("DELETE FROM rssData where rssName='{}'".format(rssName))
    conn.commit()
    conn.close()
if __name__ == "__main__":
    print(getRssTaskInfo("people"))