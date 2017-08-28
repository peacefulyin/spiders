#coding=utf-8
import requests
import json
from lxml import etree
import urllib

UserAgent = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.32',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.3 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.277.400 QQBrowser/9.4.7658.400',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER',
]
"""
headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Xsrftoken': '6a96399e-3f3f-4b67-b715-594a8c0fabe2',
    'Host': 'www.zhihu.com',
}

def get_hashid():

    url = 'https://www.zhihu.com/topics'
    gets = requests.get(url,headers=headers).text
    html = etree.HTML(gets)
    hashlist = html.xpath("//div[@class='zh-general-list clearfix']/@data-init")
    hash_id = hashlist[0]
    hash_id = '345b59e3f7ea3cc48da1245169fecc41'
    return hash_id
"""


def get_subject():
    hash_id = '345b59e3f7ea3cc48da1245169fecc41'

    url = 'https://www.zhihu.com/node/TopicsPlazzaListV2'

    headers = {
        'Host': 'www.zhihu.com',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Origin': 'https://www.zhihu.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://www.zhihu.com/topics',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    }

    data = {
        'method': 'next',
        'params': {"topic_id":3324,"offset":0,"hash_id":hash_id},
    }
    print(data)
    data = 'method=next&params=%7B%22topic_id%22%3A3324%2C%22offset%22%3A0%2C%22hash_id%22%3A%22345b59e3f7ea3cc48da1245169fecc41%22%7D'
    gets = requests.post(url, data=data, headers=headers).text
    dict = json.loads(gets)
    for each in dict.get('msg'):
        print(type(each))

def main():
    #hash_id = get_hashid()
    get_subject()
if __name__ == '__main__':
    main()