import scrapy
from bs4 import BeautifulSoup


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/#signin']

    def parse(self, response):
        soup = BeautifulSoup(response.body,'lxml')
        #print response.body.decode('utf-8').encode('gbk')
        _xsrf = soup.find('input',attrs={'name':'_xsrf'}).get('value')
        #print _xsrf+'\n'+'\n'+'\n'
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'_xsrf':_xsrf,
                        'password':'wwweee1233',
                        'captcha_type':'cn',
                        'phone_num':'18570300754',
                    },
            callback = self.deal_page
        )

    def deal_page(self,response):
        url = 'https://www.zhihu.com/people/a-dong-62-98/activities'

        yield scrapy.Request(url,callback=self.show)

    def show(self,response):
        print response.body


