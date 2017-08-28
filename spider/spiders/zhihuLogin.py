#coding=utf-8
import requests
from lxml import etree
import urllib
from urllib import parse
from jsonpath import jsonpath
import json

headers = {
    'Host':'zhuanlan.zhihu.com',
    'Connection':'keep-alive',
    'accept':'application/json, text/plain, */*',
    'X-UDID':'"AFACN0WVMAyPTm4auxMfQnj0jTciVh-e9e8=|1502198786"',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Referer':'https://zhuanlan.zhihu.com/',
}

def getspecial(offset):
    url = 'https://zhuanlan.zhihu.com/api/recommendations/columns?'
    data = {
        'limit' :'8',
        'offset':offset,
        'seed':'7',
    }
    data = parse.urlencode(data)
    url = url+data
    content = requests.get(url,headers=headers).text
    js = json.loads(content)
    slug = jsonpath(js,'$..slug')
    return slug


def gettitle(slug):
    for each in slug:
        url = 'https://zhuanlan.zhihu.com/api/columns/{}{}'.format(each,'/posts?')
        data = {
            "limit":"20",
            "offset": "0",
        }
        data = urllib.parse.urlencode(data)
        url = url + data
        contents =










def main():
    slug = getspecial(80)
    gettitle(slug)




if __name__ == '__main__':
    main()