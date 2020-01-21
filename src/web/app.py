from flask import Flask, render_template,abort, request,redirect
import webDbApi
import math
import timeago, datetime
app =Flask(__name__,static_url_path='')

@app.errorhandler(404)
def miss(e):
    (normalDict,rsshubDict)=webDbApi.getRssTasks()
    return render_template('404.html',normalDict=normalDict,rsshubDict=rsshubDict), 404

@app.route('/')
def index():
    try:
        page= request.args['page']
        page=int(page)
        page=page-1
    except:
        page=0
    if(page==""):page=0
    (normalDict,rsshubDict)=webDbApi.getRssTasks()
    pages=math.ceil(webDbApi.countAllRecords()/10)
    rssDict=webDbApi.getAllDbRssData(page*10,10)
    now = datetime.datetime.now()
    for d in rssDict:
        date = datetime.datetime.fromtimestamp(d["timestamp"])
        d["timeStr"]=timeago.format(date, now, "zh_CN")
    return render_template('rssShow.html',rssDict=rssDict,normalDict=normalDict,rsshubDict=rsshubDict,page=page+1,pages=pages)
    
@app.route('/rssShow/<string:rssName>', methods=['GET', 'POST'])
def rssName(rssName):
    page=0
    try:
        page= request.args['page']
        page=int(page)
        page=page-1
    except:
        page=0
    if(page==""):page=0
    rssDict=webDbApi.getOneDbRssData(rssName,page*10,10)
    (normalDict,rsshubDict)=webDbApi.getRssTasks()
    if (rssDict==[]):
        abort(404)
    pages=math.ceil(webDbApi.countOneRecords(rssName)/10)
    now = datetime.datetime.now()
    for d in rssDict:
        date = datetime.datetime.fromtimestamp(d["timestamp"])
        d["timeStr"]=timeago.format(date, now, "zh_CN")
    return render_template('rssShow.html',rssDict=rssDict,normalDict=normalDict,rsshubDict=rsshubDict,page=page+1,pages=pages)

@app.route("/api/addRss", methods=['GET','POST'])
def addRss():
  # GET请求
  if request.method == 'GET':
    return ""
  # POST请求
  if request.method == 'POST':
    # request.values获取数据并转化成字典
    newDict = request.values.to_dict();
    try:
        int(newDict['recommendedServerID'])
    except:
        newDict['recommendedServerID']="0"
    try:
        if (newDict['isRsshub']=="on"):
            webDbApi.addRsshubTask(newDict['url'],newDict['name'],int(newDict['round']),int(newDict['recommendedServerID']),newDict['title'])
    except:
        webDbApi.addNormalRssLink(newDict['url'],newDict['name'],int(newDict['round']),newDict['title'])
        
    return redirect('/',code=302)

@app.route("/api/updateRss", methods=['GET','POST'])
def updateRss():
  # GET请求
  if request.method == 'GET':
    return ""
  # POST请求
  if request.method == 'POST':
    # request.values获取数据并转化成字典
    newDict = request.values.to_dict();
    try:
        int(newDict['recommendedServerID'])
    except:
        newDict['recommendedServerID']="0"
    try:
        if (newDict['isRsshub']=="on"):
            webDbApi.updateRsshubTask(newDict['url'],newDict['name'],int(newDict['round']),int(newDict['recommendedServerID']),newDict['title'])
    except:
        webDbApi.updateNormalRssLink(newDict['url'],newDict['name'],int(newDict['round']),newDict['title'])
        
    return redirect('/',code=302) 

@app.route("/api/getTaskInfo", methods=['GET'])
def getTaskInfo():
    rssName=request.args['rssName']
    return webDbApi.getRssTaskInfo(rssName)

@app.route("/api/beforeDelete", methods=['GET'])
def beforeDelete():
    rssName=request.args['rssName']
    rssDict=webDbApi.getOneDbRssData(rssName,0,20)
    (normalDict,rsshubDict)=webDbApi.getRssTasks()
    now = datetime.datetime.now()
    for d in rssDict:
        date = datetime.datetime.fromtimestamp(d["timestamp"])
        d["timeStr"]=timeago.format(date, now, "zh_CN")
    return render_template('beforeDelete.html',rssDict=rssDict,normalDict=normalDict,rsshubDict=rsshubDict,rssName=rssName)

@app.route("/api/deleteRssTask", methods=['GET'])
def delRssTask():
    rssName=request.args['rssName']
    webDbApi.deleteRssTask(rssName)
    return redirect('/',code=302) 

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
