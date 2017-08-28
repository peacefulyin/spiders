#coding=utf-8
import requests
import urllib
from jsonpath import jsonpath
import json
import time


headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
'Referer':'http://search.zhenai.com/v2/search/pinterest.do',
'Accept-Encoding':'gzip, deflate',
}

def getlady(page):
    data = {
        'sex': '1',
        'agebegin': '   18',
        'ageend': ' 30',
        'workcityprovince': '-1',
        'workcitycity': '-1',
        'marriage': '   1',
        'h1': ' 150',
        'h2': ' 210',
        'salaryBegin': '-1',
        'salaryEnd': '  -1',
        'occupation': ' -1',
        'h': '  -1',
        'c': '  -1',
        'workcityprovince1': '  -1',
        'workcitycity1': '  -1',
        'constellation': '  -1',
        'animals': '-1',
        'stock': '  -1',
        'belief': ' -1',
        'lvBegin': '-1',
        'lvEnd': '  -1',
        'condition': '  66',
        'orderby': 'hpf',
        'hotIndex': '   ',
        'online': ' ',
        'currentpage': page,
        'topSearch': '  false',
    }
    url = 'http://search.zhenai.com/v2/search/getPinterestData.do?'

    data = urllib.parse.urlencode(data)
    url = url + data
    gets = requests.get(url,headers=headers).text
    js = json.loads(gets)
    print(js['data'])
    for each in js['data']:
        item = {}
        item['age'] = each.get('age')
        item['city'] = each.get('workCity')
        item['photo'] = each.get('photopath')
        item['introduce'] = each.get('introduceContent')
        print(item)
    """
    for each in jsonpath(js,'$..data'):
        item = {}
        item['age'] = jsonpath(each,'$..age')
        item['city'] = jsonpath(each, '$..workCity')
        item['photo'] = jsonpath(each, '$..photopath')
        item['introduce'] = jsonpath(each, '$..introduceContent')
        print(item)
    """

def main():
    for page in range(1,10):
        getlady(page)
        time.sleep(2)

if __name__ == '__main__':
    main()