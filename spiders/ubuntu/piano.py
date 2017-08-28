#coding=utf-8
import requests
import urllib
from jsonpath import jsonpath
import json
import time
import os
import threading
from Queue import Queue

headers = {
'Host':'api.popiano.org',
'Connection':'keep-alive',
'Accept':'application/json',
'User-Agent':'hanon/14 (iPad; iOS 10.3.2; Scale/2.00)',
'Accept-Language':'zh-Hans-CN;q=1',
}


class ThreadCrawl(threading.Thread):
    def __init__(self,threadName,Pque):
        #threading.Thread.__init__(self)
        # 调用父类初始化方法
        super(ThreadCrawl, self).__init__()
        # 线程名

        self.threadName = threadName
        self.Pque = Pque

        # 请求报头
        self.headers = {"User-Agent" : "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}

    def run(self):
        print self.threadName+"启动了"
        if not self.Pque.empty():
            url = self.Pque.get(False)
            print url
            contents = requests.get(url, headers=headers).text
            js = json.loads(contents)
            titles = jsonpath(js, '$..title')
            ids = jsonpath(js, '$..id')
            for i in range(len(titles)):
                title = titles[i]
                id = ids[i]
                print '现在的曲单是'+ title.encode('utf-8')
                getlist(title, id)
                time.sleep(2)




def getstypes(Pque):
    url = 'http://api.popiano.org/album/albumCategorys?'
    data = {
        'hd': '0',
        'platform': 'ipad',
        'appver': '1.3.2',
        'channel': 'ios',
    }
    data = urllib.urlencode(data)
    url = url+data
    contents = requests.get(url,headers=headers).text
    js = json.loads(contents)
    ids = jsonpath(js,'$..id')
    for id in ids:
        getlinks(id,data,Pque)

def getlinks(id,data,Pque):
    url = 'http://api.popiano.org/album/ac-%s?'%id
    url = url+data
    Pque.put(url)



def getlist(title,id):
    url = 'http://api.popiano.org/album/songs?'
    data = {'hd':'0',
            'platform':'ipad',
            'appver':'1.3.2',
            'channel':'ios',
            'album':id,
            'limit':'160002',}
    data = urllib.urlencode(data)
    url = url+data

    contents = requests.get(url,headers=headers).text
    #print contents
    js = json.loads(contents)
    images = jsonpath(js,'$..images')
    titles = jsonpath(js, '$..title')

    next = 0
    for i in images:
        imagelinks = jsonpath(i,'$..fullPath')
        isExists = os.path.exists('./'+title+'/')
        if not isExists:
            os.mkdir('./'+title)
        name = titles[next]
        print '正在下载'+name.encode('utf-8')
        next+=1
        down(imagelinks,name,title)

def down(imagelinks,name,title):
    headers = {
        'Host': '7u2gah.com1.z0.glb.clouddn.com',
        'Connection': 'keep-alive',
        'Accept': 'image/*;q=0.8',
        'User-Agent': 'hanon/14 CFNetwork/811.5.4 Darwin/16.6.0',
        'Accept-Language': 'zh-cn',
    }
    page = 1
    for each in imagelinks:
        isExists = os.path.exists('./'+title+'/'+name+'/')
        if not isExists:
            os.mkdir('./'+title+'/'+name+'/')
        image = requests.get(each,headers=headers).content
        with open('./'+title+'/'+name+'/'+str(page)+'.png','wb') as f:
            f.write(image)
            time.sleep(0.3)
        page+=1


def main():
    Pque = Queue()
    getstypes(Pque)
    lock = threading.Lock()

    # 三个采集线程的名字
    crawlList = ["采集线程1号", "采集线程2号", "采集线程3号"]
    # 存储三个采集线程的列表集合
    threadcrawl = []
    for threadName in crawlList:
        thread = ThreadCrawl(threadName, Pque)
        thread.start()
        threadcrawl.append(thread)

    for i in threadcrawl:
        i.join()


if __name__ == '__main__':
    main()