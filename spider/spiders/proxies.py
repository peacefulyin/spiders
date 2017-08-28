#coding=utf-8
import requests
from lxml import etree
import time
from queue import Queue
import threading
from threading import Lock

class Xici(object):
    def __init__(self,offset,list):
        self.url = 'http://www.xicidaili.com/nn/'
        self.offset = offset
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
        self.Que = Queue()
        self.list = list
        self.threads = []
        self.lock =Lock()

    def getproxies(self):
        for i in range(1,self.offset):
            content = requests.get(self.url+str(self.offset),headers=self.headers).text
            html = etree.HTML(content)
            for each in html.xpath("//table[@id='ip_list']//tr[1]/following-sibling::*"):
                print('1')
                item = {}
                item['ip'] = each.xpath('./td[2]/text()')[0]
                item['port'] = each.xpath('./td[3]/text()')[0]
                item['type'] = each.xpath('./td[6]/text()')[0]
                self.Que.put(item)
            time.sleep(1)

        t1 = threading.Thread(target=self.vertification,args=('1号',))
        self.threads.append(t1)
        t2 = threading.Thread(target=self.vertification,args=('2号',))
        self.threads.append(t2)
        t3 = threading.Thread(target=self.vertification,args=('3号',))
        self.threads.append(t3)
        for t in self.threads:
            t.start()
        for t in self.threads:
            t.join()

    def vertification(self,name):
        print(name+'进来了')
        url = 'https://www.baidu.com'
        proxies = {}
        while not self.Que.empty():
            with self.lock:
                proxy = self.Que.get()
            if proxy['type'] == 'HTTP':
                proxies = {'http':'http://'+proxy['ip']+':'+proxy['port']}
                print(proxies)
                try:
                    gets = requests.get(url,headers=self.headers,proxies=proxies)
                    print(gets.status_code)
                    if gets.status_code==200:
                        self.list.append(proxies)
                    time.sleep(0.3)
                except Exception:
                    print('下一位')
list = []
xici = Xici(5,list)
xici.getproxies()
with open('proxy.txt','w') as f:
    f.write(str(list))

