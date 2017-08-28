# -*- coding: utf-8 -*-
import scrapy


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['www.renren.com']
    start_urls = ['http://www.renren.com/SysHome.do']

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'email':'...','password':'...'},
            callback = self.parse_page
        )

    def parse_page(self,response):
        url = 'http://www.renren.com/947521844/profile'
        yield scrapy.Request(url,callback=self.parse_newpage)


    def parse_newpage(self,response):
        print response.url
        print response.body.decode('utf-8').encode('gbk')

