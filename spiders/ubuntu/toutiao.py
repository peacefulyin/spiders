#coding=utf-8
import requests
import urllib
from jsonpath import jsonpath
import json

class jiepai(object):
    def __init__(self,offset):
        self.data = {
            'offset':offset,
            'format': 'json',
            'keyword': '街拍',
            'autoload': 'true',
            'count': '20',
            'cur_tab': '1',
        }
        self.headers= {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
        self.url = 'http://www.toutiao.com/search_content/?'+urllib.urlencode(self.data)

    def getslink(self):
        gets = requests.get(self.url,headers=self.headers)
        new = json.loads(gets.text)
        return new.get('data')


jie = jiepai(20)

ht = jie.getslink()
for i in ht:
    print i

