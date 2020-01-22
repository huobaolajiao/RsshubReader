# RsshubReader
 基于Python开发的RSS阅读器，此外本项目还可以通过[RSShub](https://github.com/DIYgod/RSSHub)的router，选择可用的服务器（官方演示服务器，公开搭建的服务器以及自建服务器）抓取RSS源。
 ![RsshubReader](https://github.com/huobaolajiao/RsshubReader/blob/master/img/WebRss.png)
 ![RsshubReader]( https://github.com/huobaolajiao/RsshubReader/blob/master/img/editRss.png)
 
 项目后端使用feedparser解析rss源，flask作为网页后端，前端由于没有体系地学过，很多都是东拼西凑，使用了[pro-sidebar-template](https://github.com/azouaoui-med/pro-sidebar-template)，[ButtonComponentMorph](https://github.com/codrops/ButtonComponentMorph)，在此感谢。

## 原理
* rssSpider按照更新周期，一般设置3600秒或600秒爬取rss源，downloadDouyinVideo是一个拓展功能，可以保存某平台视频到本地，未来可以增加更多功能。

* web/app.py是flask的服务器主程序

*rsshubReaderMonitor.pyw是配合win32服务的监视器
 ![RsshubReaderMonitor](https://github.com/huobaolajiao/RsshubReader/blob/master/img/monitor.png)
## 使用教程
```
# 0. requirements
pip install -r requirements.txt
# 1. run spider
手动前台循环抓取订阅
RsshubReader/src/spider/manualLoop.py
or
windows平台下利用pywin32加载为服务，可开机自启
RsshubReader/src/spider/rsshubServers.py
# 2. run web server
RsshubReader/src/web/app.py
# 3.web browser
127.0.0.1:5000
```

## 已知问题
 1,python工程目录结构import包比较困难。
 
 import sys
 sys.path.append("..")
 
 有时候要设置绝对路径，不方便用户移植（可直接运行教程里的manualLoop和app脚本，但win32工作目录会跑到系统目录....233333），待优化
 
 2,前端代码东拼西凑，有css和js直接写在html里甚至直接挂在标签属性上，有机会优化

 3,rss订阅源Name(内部主键)不能随意在用户web界面修改，一般修改标题title，只能在数据库修改或者删除后重新添加任务，但此参数一般前台不可见。
## 依赖的库
``` 
 pywin32==227
 timeago==1.0.13
 requests==2.22.0
 pytz==2019.3
 feedparser==5.2.1
 Flask==1.1.1
 ```
 
## 使用许可
This code is released under the [MIT](https://github.com/azouaoui-med/pro-sidebar-template/blob/gh-pages/LICENSE) license.

©huobaolajiao
