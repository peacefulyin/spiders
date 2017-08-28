# -*- coding: utf-8 -*-
import scrapy


class LvSpider(scrapy.Spider):
    name = 'lv'
    allowed_domains = ['www.33lc.com']


    def start_requests(self):
        url = 'http://www.33lc.com/index.php?m=lc_search&c=index&a=pc&page='
        offset = 1
        for i in range(1,5):
            yield scrapy.Request(url+str(offset),callback=self.parse_link)
            offset+=1

    def parse_link(self, response):
        urls = response.css('.soft_list .tit a::attr(href)').extract()
        print('\n'*10)
        for each in urls:
            url = 'http://www.33lc.com'+each
            yield scrapy.Request(url,callback=self.deal_soft)

    def deal_soft(self,response):
        item = {}
        item['name'] = response.xpath("//div[@id='soft_title']/text()").extract()[0]
        item['urls'] = response.xpath("//div[@class='sort_list']//@href").extract()
        yield item
