# -*- coding: utf-8 -*-
import scrapy


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['https://www.taobao.com']

    url = 'https://s.taobao.com/search?q=NIKE&bcoffset=4&ntoffset=4&p4ppushleft=1%2C48&s=0'

    start_urls = [url]


    def parse(self, response):
        total = response.css('.wraper .inner .total::text').extract_first()
        print(response.body)
        print('\n'*5)
        print(total)
