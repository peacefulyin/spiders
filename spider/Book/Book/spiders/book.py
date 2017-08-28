# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import urllib
from Book.items import BookItem

class BookSpider(CrawlSpider):
    name = 'book'
    allowed_domains = ['www.readnovel.com']
    url = 'https://www.readnovel.com/free/all?'
    data = {
        'pageNum': '1',
        'pageSize': '10',
        'gender': '2',
        'catId': '-1',
        'isFinish': '-1',
        'isVip': '1',
        'size': '-1',
        'updT': '-1',
        'orderBy': '0',
    }
    data = urllib.urlencode(data)


    start_urls = [url+data]
    level1 = LinkExtractor(allow=r'/book/\d+')
    level2 = LinkExtractor(allow=r'www.readnovel.com/chapter/\d+/\d+')
    rules = (
        Rule(level1, follow=True),
        Rule(level2,callback='parse_item',follow=True),
    )

    def parse_item(self, response):
        i = BookItem()

        i['chapter'] = response.xpath(r'//h3/text()').extract()[0]
        i['text'] = ','.join(response.xpath("//div[@class='read-content j_readContent']//p/text()").extract())
        return i
