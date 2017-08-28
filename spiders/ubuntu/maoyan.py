#coding=utf-8

import time
from lxml import etree
import urllib2
import json
offset = 0
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
url = 'http://maoyan.com/board/4?offset='
requests = urllib2.Request(url+str(offset),headers=headers)
response = urllib2.urlopen(requests)
html = etree.HTML(response.read())

list = []
for i in html.xpath("//div[@class='board-item-main']"):
    item = {}
    item['title'] = i.xpath(".//a/text()")[0]
    item['actors'] = i.xpath(".//p[@class='star']/text()")[0]

    tjson = json.dumps(item,ensure_ascii=False)
    with open('1.txt', 'a') as f:
        f.write(tjson.encode('utf-8') +'\n')
