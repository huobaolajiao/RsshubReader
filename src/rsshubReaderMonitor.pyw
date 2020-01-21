# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 20:27:30 2020

@author: wangyouqish
"""
import tkinter as tk
import win32service
import win32serviceutil
import time
import threading
import os

def GetTxtLastLine(inputfile) :
    filesize = os.path.getsize(inputfile)
    blocksize = 1024
    dat_file = open(inputfile, 'r')
    last_line = ""
    if filesize > blocksize :
        maxseekpoint = (filesize // blocksize)
        dat_file.seek((maxseekpoint-1)*blocksize)
    elif filesize :
        #maxseekpoint = blocksize % filesize
        dat_file.seek(0, 0)
    lines = dat_file.readlines()
    if lines:
        last_line = lines[-1].strip()
        #print "last line : ", last_line
        dat_file.close()
        return last_line
def GetSvcStatus(svcname):
    svcstatusdic = {
    #The service continue is pending.
    win32service.SERVICE_CONTINUE_PENDING:"continue pending", 
    #The service pause is pending.
    win32service.SERVICE_PAUSE_PENDING:"pause pending",
    #The service is paused.
    win32service.SERVICE_PAUSED:"paused" , 
    #The service is running.
    win32service.SERVICE_RUNNING:"running",
    #The service is starting.
    win32service.SERVICE_START_PENDING:"start pending", 
    # The service is stopping.
    win32service.SERVICE_STOP_PENDING:"stop pending" ,
    #The service is not running.
    win32service.SERVICE_STOPPED:"stoped"
    }
    try:
        status = win32serviceutil.QueryServiceStatus(svcname)
        if status:
            return svcstatusdic.get(status[1],"unknown")
        else:
            return "else"
    except:
        return "error"
class App:
    
    def __init__(self, root):
        self.frame1 = tk.Frame(root)
        self.frame1.pack(side=tk.TOP,anchor=tk.W)
        self.v = tk.StringVar()
        self.v.set('服务状态：   '+status)
        self.v2 = tk.StringVar()
        self.v2.set('rssSpider Log：   ')
        self.v3 = tk.StringVar()
        self.v3.set('dyDownLoad Log：   ')
        self.Label1= tk.Label(self.frame1, textvariable=self.v, height=1)
        self.Label1.pack(side=tk.LEFT,anchor=tk.W)
        self.Button1=tk.Button(self.frame1,height = 1,width = 10,text="开启服务", command=self.startService)
        self.Button1.pack(side=tk.LEFT,anchor=tk.W,padx=10,pady=10)
        self.Button2=tk.Button(self.frame1,height = 1,width = 10,text="关闭服务", command=self.stopService)
        self.Button2.pack(side=tk.LEFT,anchor=tk.W,padx=10,pady=10)
        t= threading.Thread(target=self.updateStatus)
        self.Label2= tk.Label(root, textvariable=self.v2, height=1)
        self.Label2.pack(side=tk.TOP,anchor=tk.W)
        self.Label3= tk.Label(root, textvariable=self.v3, height=1)
        self.Label3.pack(side=tk.TOP,anchor=tk.W)
        t.start()
    def startService(self):
        try:
            win32serviceutil.StartService(svcname)
        except:
            pass
    def stopService(self):
        try:
            win32serviceutil.StopService(svcname)
        except:
            pass
        '''win32serviceutil.StopService(svcname)关
            win32serviceutil.StartService(svcname)开
            RemoveService(serviceName)  #删除服务
            RestartService(serviceName, args = None, waitSeconds = 30, machine = None) #重启服务
            InstallService(pythonClassString, serviceName, displayName)  #安装服务'''
        
    def updateStatus(self):
        while(1):
            time.sleep(1)
            status = GetSvcStatus(svcname)
            #print("{} current status : {}".format(svcname,status))
            self.v.set('服务状态：   '+status)
            if(status=="running"):
                self.Button1.configure(state='disabled')
                self.Button2.configure(state='normal')
            if(status=="stoped"):
                self.Button1.configure(state='normal')
                self.Button2.configure(state='disabled') 
            if(status=="stop pending" or status=="start pending" or status=="continue pending" or status=="paused"):
                self.Button1.configure(state='disabled')
                self.Button2.configure(state='disabled')
            temp="rssSpider Log：   "+GetTxtLastLine(os.path.join("log","rssSpider.txt"))
            self.v2.set(temp)
            temp="dyDownLoad Log：   "+GetTxtLastLine(os.path.join("log","dyDownload.txt"))
            self.v3.set(temp)
    
    

if __name__ == '__main__':
    svcname = "RssSpiderService"
    status = GetSvcStatus(svcname)
    #print("{} current status : {}".format(svcname,status))
    
    root = tk.Tk()
    app = App(root)
    
    root.title('RsshubReaderMonitor')  # 设置窗体的标题栏
    # 开始主事件循环
    root.mainloop()