#coding=utf-8
import requests
from requests.exceptions import ProxyError
import time
from lxml import etree
import re
import random



def links(page):
    headers = {
        'Host': 'www.mzitu.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://www.mzitu.com/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    }
    url = 'http://www.mzitu.com/page/%d'%page
    gets = requests.get(url,headers=headers)
    html = etree.HTML(gets.text)
    pages = html.xpath("//div[@class='postlist']//li/a/@href")
    getin(pages)

def getin(pages):
    headers = {
        'Host': 'www.mzitu.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://www.mzitu.com/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    }
    for i in pages:
        print(i,'他好')
        for j in range(1,4):
            print(i+'/'+str(j),'你好')
            gets = requests.get(i+'/'+str(j),headers=headers)
            html = etree.HTML(gets.text)
            images = html.xpath("//div[@class='main-image']//img/@src")
            download(images,i)


def download(images,i):
    headers = {
        'Host': 'i.meizitu.net',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer':i,
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    }
    for i in images:
        print(i)
        gets = requests.get(i,headers=headers)
        time.sleep(2)
        with open(i[-9:].replace('/','.'),'wb')as f:
           f.write(gets.content)





if __name__ == '__main__':

    for i in range(3,100):
        links(i)

'http://i.meizitu.net/2017/08/22b01.jpg'
'http://i.meizitu.net/2017/08/22b01.jpg'