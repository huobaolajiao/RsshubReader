# RsshubReader
 基于Python开发的RSS阅读器，此外本项目还可以通过[RSShub](https://github.com/DIYgod/RSSHub)的router，选择可用的服务器（官方演示服务器，公开搭建的服务器以及自建服务器）抓取RSS源。
 ![RsshubReader](https://github.com/huobaolajiao/RsshubReader/blob/master/img/WebRss.png)
 ![RsshubReader]( https://github.com/huobaolajiao/RsshubReader/blob/master/img/editRss.png)
 
 项目后端使用feedparser解析rss源，flask作为网页后端，前端由于没有体系地学过，很多都是东拼西凑，使用了[pro-sidebar-template](https://github.com/azouaoui-med/pro-sidebar-template)，[ButtonComponentMorph](https://github.com/codrops/ButtonComponentMorph)，在此感谢。

## 原理
* rssSpider按照更新周期，一般设置3600秒或600秒爬取rss源，downloadDouyinVideo是一个拓展功能，可以保存某平台视频到本地，未来可以增加更多功能。

* web/app.py是flask的服务器主程序

* rsshubReaderMonitor.pyw是配合win32服务的监视器
 ![RsshubReaderMonitor](https://github.com/huobaolajiao/RsshubReader/blob/master/img/monitor.png)
## 使用教程
```
# 0. requirements
pip install -r requirements.txt
# 1. run spider
A手动前台循环抓取订阅
RsshubReader/src/spider/manualLoop.py
B或者windows平台下利用pywin32加载为服务可开机自启
python RsshubReader/src/spider/SpiderService.py --startup auto install   其他常用操作：stop，start，remove
# 2. run web server
RsshubReader/src/web/app.py
# 3.web browser
127.0.0.1:5000
```

## 已知问题
 1,python不同工程目录（log，database，spider，web）有相互调用。
  
 一般可直接运行教程里的manualLoop.py和app.py脚本启动爬虫和服务器。但win32服务时工作目录会跑到系统目录，可能要设置绝对路径，不方便用户移植，待优化（请教各位大神怎么标准import自己的py，或者未来config文件定义项目根目录）
 
 2,rss订阅源Name(数据库及目录结构主键)不能随意在用户web界面修改(一般只修改标题title)，强行修改可能导致部分功能出错，但此参数在前台不可见，仅在设置时需要操心。
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
