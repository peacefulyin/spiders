#coding=utf-8
import requests
import time
import json

class hungry(object):
    def __init__(self):
        self.headers = {
            'Host': 'www.ele.me',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        }
        self.offset = 0

    def rollpage(self):
        while True:
            url = 'https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash=wt021zf695x&latitude=28.16802&limit=24&longitude=112.93161&offset={}&terminal=web'.format(str(self.offset))
            gets = requests.get(url, headers=self.headers).text
            if gets:
                dict = json.loads(gets)
                print(dict)
                self.get_shop(dict)
                time.sleep(5)
                self.offset+=20
            else:
                break

    def get_shop(self,dict):
        for each in dict:
            item = {}
            item['店名'] = each.get('name')
            item['活动'] = each.get('activities')
            item['地址'] = each.get('address')
            item['描述'] = each.get('description')
            item['距离'] = each.get('distance')
            item['id'] = each.get('id')
            item['手机'] = each.get('phone')
            item['详情'] = each.get('promotion_info')
            item['销量'] = each.get('rencent_order_num')
            item['评分'] = each.get('rating')
            self.get_foods(item)
            time.sleep(5)

    def get_foods(self,item):
        url = 'https://www.ele.me/restapi/shopping/v2/menu?restaurant_id='+str(item.get('id'))
        gets = requests.get(url,headers=self.headers).text
        if gets:
            dict = json.loads(gets)
            item['foods'] = dict
        print(item)


test = hungry()
test.rollpage()