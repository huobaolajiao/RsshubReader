# encoding=utf-8
import win32serviceutil
import win32service
import win32event
import sys
sys.path.append('D:\\infohub\\rssReader')
import os
import time
class rssSpiderService(win32serviceutil.ServiceFramework):
    _svc_name_ = "RssSpiderService"
    _svc_display_name_ = "Rss Spider Service"
    _svc_description_ = "rss Spider Service"
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.isAlive = True

    def SvcDoRun(self):
        import autoDownloader.downloadDouyinVideo as downloadDouyinVideo
        import spider.rssSpider as rssSpider
        import log.logCenter as logCenter
        logger=logCenter.getLogger("service")
        while(self.isAlive):
            try:
                rssSpider.getAllRssData()
                downloadDouyinVideo.downloadAllVideo()
                logger.info("alive")
                time.sleep(60)
            except:
                logger.error("execute error")
    
      
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.isAlive = False
  
  
if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(rssSpiderService) 