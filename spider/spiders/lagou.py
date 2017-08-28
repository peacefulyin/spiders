#coding=utf-8
import requests
import urllib
import jsonpath
import json
import random
from lxml import etree
import time



position = input('职位:')

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




headers = {
'Host':'www.lagou.com',
'Connection':'keep-alive',
'Origin':'https://www.lagou.com',
'X-Anit-Forge-Code':'0',
'User-Agent':random.choice(UserAgent),
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
'Accept':'application/json, text/javascript, */*; q=0.01',
'X-Requested-With':'XMLHttpRequest',
'X-Anit-Forge-Token':'None',
'Referer':'https://www.lagou.com/jobs/list_%s?labelWords=&fromSearch=true&suginput='%position,
'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
}
with open('proxy.txt') as f:
    proxy = eval(f.read())




def getlink(page):
    data = {
        'pn': page,
        'kd': position,
        'first': 'false',
    }
    data = urllib.parse.urlencode(data)
    url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'
    proxies = random.choice(proxy)
    print(proxies)
    try:
        content = requests.post(url,data=data,headers=headers,proxies=proxies).text
        js = json.loads(content)
        for each in jsonpath.jsonpath(js,'$..hrInfoMap'):
            item = {}
            item['company'] = jsonpath.jsonpath(each, '$..companyFullName')
            item['job'] = jsonpath.jsonpath(each, '$..positionName')
            item['salary'] = jsonpath.jsonpath(each, '$..salary')
            city = jsonpath.jsonpath(each, '$..city')
            address = jsonpath.jsonpath(each, '$..district')
            list.append(item)
        time.sleep(2)
    except Exception:
        getlink(page)


print(list)
with open(position+'.txt','w') as f:
    f.write(str(list))





list = []
for page in range(1,7):
    getlink (page)

