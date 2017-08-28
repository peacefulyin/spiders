#coding=utf-8
import requests
import urllib
import re
import json
from jsonpath import jsonpath
import time
import pymongo

MONGO_URL = 'localhost'
MONGO_DB = 'zhihu'

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
Set = set()

def getlist(offset):
    headers = {
        'Host': 'zhuanlan.zhihu.com',
        'Connection': 'keep-alive',
        'accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Referer': 'https://zhuanlan.zhihu.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',

    }
    url = 'https://zhuanlan.zhihu.com/api/recommendations/columns?'
    data = {
        'limit': '8',
        'offset':offset,
        'seed': '7',
    }
    data = urllib.parse.urlencode(data)
    url = url + data
    gets = requests.get(url,headers=headers).text
    list = json.loads(gets)
    getTopic(list)

def getTopic(list):
    for each in list:
        item = {}
        item['name'] = each.get('name')
        item['url'] = each.get('url')
        item['postsCount'] = each.get('postsCount')
        item['description'] = each.get('description')
        if item['url'] in Set:
            Set.add(item['url'])
            getSpecial(item)

def getSpecial(item):
    count = item['postsCount']
    offset = 0

    while count >= 0:
        headers = {
            'Host': 'zhuanlan.zhihu.com',
            'Connection': 'keep-alive',
            'accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Referer': 'https://zhuanlan.zhihu.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',

        }
        url = 'https://zhuanlan.zhihu.com'+item['url']
        url = 'https://zhuanlan.zhihu.com/api/columns{}/posts?'.format(item['url'])

        data = {
            'limit': '20',
            'offset': offset,
        }
        data = urllib.parse.urlencode(data)

        url = url + data
        gets = requests.get(url,headers=headers).text
        Alist = json.loads(gets)
        time.sleep(3)
        name = item['name']
        getArtical(Alist,name)
        count -= 20
        offset +=20


def getArtical(Alist,name):
    for each in Alist:
        item = {}
        item['title'] = each.get('title')
        item['url'] = each.get('url')
        item['time'] = each.get('publishedTime')
        item['content'] = each.get('content').replace('</p>','\n')
        content = rep.sub('',item['content'])
        item['content'] = content

        save_to_mongo(item,name)

def save_to_mongo(item,name):
    if db[name].insert(item):
        print('success to save')


rep = re.compile(r'(<.*?>)', re.S)


def main():
    for offset in range(0,1000):
        getlist(offset)

if __name__ == '__main__':
    main()