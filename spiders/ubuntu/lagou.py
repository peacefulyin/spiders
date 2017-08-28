#coding=utf-8
import requests
import json
import jsonpath
import time

headers = {"Host":"www.lagou.com",
"Connection":"keep-alive",
"Origin":"https://www.lagou.com",
"X-Anit-Forge-Code":"0",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
"Accept":"application/json, text/javascript, */*; q=0.01",
"X-Requested-With":"XMLHttpRequest",
"X-Anit-Forge-Token":"None",
"Referer":"https://www.lagou.com/jobs/list_python?city=%E6%B7%B1%E5%9C%B3&cl=false&fromSearch=true&labelWords=&suginput=",
"Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
"Cookie":"user_trace_token=20170711134437-739043a813fa42df90ffd54fa8003af9; LGUID=20170711134437-069de198-65fc-11e7-a963-525400f775ce; JSESSIONID=ABAAABAAAGFABEF932614583490EDD6565B3B5B38EEA086; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Da0zgd1BJ1htlUrLQ_WO71GvyuyBDGS0mj1VqQ_mpEF_%26wd%3D%26eqid%3Da943f409000462a100000005597442f1; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; index_location_city=%E6%B7%B1%E5%9C%B3; TG-TRACK-CODE=index_search; SEARCH_ID=da759bcadfdc4bd7a19146a84160efe5; _ga=GA1.2.918474463.1499751871; _gat=1; LGSID=20170723143220-ae230c45-6f70-11e7-a23b-525400f775ce; LGRID=20170723144420-5b1b6f46-6f72-11e7-b393-5254005c3644",}
url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false '

while True:
    b = 1
    data = {
        'first': 'false',
        'kd': 'python',
        'pn': b,
    }
    gets = requests.get(url,data=data,headers=headers).text
    html = json.loads(gets)
    list =jsonpath.jsonpath(html,'$..result')
    list1 = []
    for i in list[0]:
        item = {}
        item['positon'] = i['positionName']
        item['require'] = i['workYear'] + ':' + i['education']
        item['payment'] = i['salary']
        list1.append(item)
    print( list1)

    for i in list1:
        with open('1.txt','a') as f:
            a = str(i)
            f.write(a+'\n')
    b+=1
    time.sleep(2)




