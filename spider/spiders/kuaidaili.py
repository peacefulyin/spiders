#coding=utf-8
import requests
from lxml import etree
import time
from queue import Queue
import threading
from threading import Lock
from bs4 import BeautifulSoup

class KuaiDaiLi(object):
    def __init__(self,offset):
        self.url = 'http://www.kuaidaili.com/free/inha/'
        self.offset = offset
        self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
        self.Que = Queue()
        self.list = []
        self.threads = []
        self.lock =Lock()

    def getproxies(self):
        for i in range(1,self.offset):
            content = requests.get(self.url+str(self.offset),headers=self.headers).text
            time.sleep(2)
            soup = BeautifulSoup(content,'lxml')
            tr = soup.select('#list tr')
            for row in tr:
                cell = [i.text for i in row.select('td')]
                if cell:
                    self.Que.put(cell)
                    print(cell)
        t1 = threading.Thread(target=self.vertification,args=('1号',))
        self.threads.append(t1)
        t2 = threading.Thread(target=self.vertification,args=('2号',))
        self.threads.append(t2)
        t3 = threading.Thread(target=self.vertification,args=('3号',))
        self.threads.append(t3)
        for t in self.threads:
            print(1)
            t.start()
        for t in self.threads:
            print(2)
            t.join()
        return self.list
    def vertification(self,name):
        print(name+'进来了')
        url = 'www.baidu.com'
        proxies = {}
        while not self.Que.empty():
            with self.lock:
                proxy = self.Que.get()
            if proxy[3] == 'HTTP':
                proxies = {'http':'http://'+proxy[0]+':'+proxy[1]}
                print(proxies)

                try:
                    url = 'https://www.baidu.com'
                    gets = requests.get(url,headers=self.headers,proxies=proxies)
                    print(gets.status_code)
                    if gets.status_code==200:
                        self.list.append(proxies)
                    time.sleep(0.3)
                except Exception:
                    print('下一位')

kuai = KuaiDaiLi(2)
list = kuai.getproxies()
with open('proxys.txt','w') as f:
    f.write(str(list))