# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 20:51:00 2020

@author: wangyouqish
"""
import sys
sys.path.append("..")
import time
import json
import requests
import re
import threading
import database.dbConn as dbConn
import log.logCenter as logCenter

def getFuncNum(ServerAD):
    try:
        pingAdress=ServerAD+"/api/routes"
        head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0'}
        page = requests.get(pingAdress, headers=head,timeout=(10,10))
        page.encoding = 'utf-8'
        page_content = page.text
        data = json.loads(page_content)
        FN = re.findall( r'\d+',data['message'] )[0]
        #logger.info(ServerAD+" "+FN+" functions")
        return int(FN)
    except:
        logger.error(ServerAD+" ping failed")
        return 0
def addServer(ID,ServerAD):
    conn=dbConn.getConn()
    FC= time.strftime("%Y-%m-%d",time.localtime())
    LC= time.strftime("%Y-%m-%d",time.localtime())
    try:
        FN=getFuncNum(ServerAD)
        conn.execute("INSERT INTO rsshubServers (ID,Adress,FuncNum,FirstCheck,LastCheck) VALUES ({},'{}',{},'{}','{}')".format(ID,ServerAD,FN,FC,LC))
    except:
        logger.error("AddFailed  "+ServerAD)
    conn.commit()
    conn.close()
def updateOneServer(ID,ServerAD):
    conn=dbConn.getConn()
    LC= time.strftime("%Y-%m-%d",time.localtime())
    try:
        FN=getFuncNum(ServerAD)
        if(FN==0):
            FN=getFuncNum(ServerAD)
            if(FN==0):
                conn.close()
                return 
        sqlupdate="UPDATE rsshubServers set FuncNum={},LastCheck ='{}'  where ID={}".format(FN,LC,ID)
        conn.execute(sqlupdate)
        conn.commit()
        logger.info("Updatedone  "+ServerAD+"  "+str(FN)+"个功能")
    except:
        logger.error("UpdateFailed  "+ServerAD)
    conn.close()
def updateAllServers():
    conn=dbConn.getConn()
    c = conn.cursor()
    #Ad= input()
    cursor = c.execute("SELECT ID,Adress from rsshubServers")
    thread_list = []
    for row in cursor:
        t= threading.Thread(target=updateOneServer,args=(row[0],row[1]))
        t.start()
        thread_list.append(t)
    
    
    for t in thread_list:
        t.join()
    conn.close()
    logCenter.destroyLogger(logger)

logger=logCenter.getLogger("rsshubServer")
if __name__ == "__main__":
    updateAllServers()

