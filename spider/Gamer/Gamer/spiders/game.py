# -*- coding: utf-8 -*-
import scrapy


class GameSpider(scrapy.Spider):
    name = 'game'
    allowed_domains = ['www.gamersky.com']
    url = 'http://down.gamersky.com/pc/?sort=10&list='
    offset = 1
    start_urls = [url+str(offset)]

    def start_requests(self,):
        url = 'http://down.gamersky.com/pc/?sort=10&list='
        offset = 1
        url = url+str(offset)
        yield scrapy.Request(url, callback=self.deal_page)



    def deal_page(self,response):
        links = response.css('.downData .tit a::attr(href)').extract()
        for each in links:
            print(each)
            yield scrapy.Request(each, callback=self.deal)

    def deal(self,response):
        print(response.url)
        print('\n'*20)
        item = {}
        item['name'] = response.xpath("//div[@class='Mid2L_actdl2']//div[@class='tit']/text()").extract_first()
        item['url'] = response.xpath("//div[@class='Download']//div[@class='dl_url']//@href").extract()
        print(item)
        yield item