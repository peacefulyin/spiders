#coding=utf-8
import scrapy
from Xici.items import XiciItem

class XiciSpider(scrapy.Spider):
    name = 'xici'
    allowed_domains = ['www.xicidaili.com']
    offset = 1
    url = 'http://www.xicidaili.com/nn/'
    start_urls = [url+str(offset)]


    def parse(self, response):
        for each in response.xpath("//table[@id='ip_list']//tr[1]/following-sibling::*"):
            item = XiciItem()
            item['ip'] = each.xpath('./td[2]/text()').extract()[0]
            item['port'] = each.xpath('./td[3]/text()').extract()[0]
            item['type'] = each.xpath('./td[6]/text()').extract()[0]
            yield item
        if self.offset <505:
            self.offset+=1
        yield scrapy.Request(self.url+str(self.offset),callback=self.parse)





