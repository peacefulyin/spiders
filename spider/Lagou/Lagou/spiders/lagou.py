# -*- coding: utf-8 -*-
import scrapy
import time
import urllib
import json
from jsonpath import jsonpath

class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    #start_urls = ['http://www.lagou.com/']
    offset = 1
    headers = {
            'Host':'www.lagou.com',
            'Connection':'keep-alive',
            'Content-Length':'26',
            'Origin':'https://www.lagou.com',
            'X-Anit-Forge-Code':'0',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With':'XMLHttpRequest',
            'X-Anit-Forge-Token':'None',
            'Referer':'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
            'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
            }

    def start_requests(self):
        data =  {
                'pn': 1,
                'kd': 'python',
                'first': 'false',
            }
        data = urllib.urlencode(data)

        print '1'
        return [scrapy.FormRequest(
            url='https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false',
            formdata =data,
            callback= self.parse_page,
            headers=self.headers
        )]

    def parse_page(self, response):
        print 3
        print response.body+'\n'+'\n'+'\n'+'\n'
        yield response.body
