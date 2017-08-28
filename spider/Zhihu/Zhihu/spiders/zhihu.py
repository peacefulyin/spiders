# -*- coding: utf-8 -*-
import scrapy
import urllib
import json

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    def start_requests(self):
        followeeurl = 'https://www.zhihu.com/api/v4/members/excited-vczh/followees?'
        followersurl = 'https://www.zhihu.com/api/v4/members/excited-vczh/followers?'
        data = {
            'include': 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics',
            'offset': '0',
            'limit': '20',
        }
        data = urllib.parse.urlencode(data)
        followeeurl = followeeurl + data
        followerurl = followersurl + data
        yield scrapy.Request(followeeurl,callback=self.followee)
        yield scrapy.Request(followerurl,callback=self.followerurl)

    def followee(self,response):
        results = json.loads(response.text)
        for result in results['data']:
            id = result['url_token']
            meta = {'id':id}
            url = 'https://www.zhihu.com/people/'+id +'/followers'
            yield scrapy.Request(url,meta=meta,callback=self.get_info)
        if results.get('paging').get('is_end') ==False:
            yield scrapy.Request(results.get('paging').get('next'),callback=self.followee)

    def follower(self,response):
        results = json.loads(response.text)
        for result in results['data']:
            id = result['url_token']
            meta = {'id':id}
            url = 'https://www.zhihu.com/people/'+id +'/followers'
            yield scrapy.Request(url,meta=meta,callback=self.get_info)

        if results.get('paging').get('is_end') == False:
            yield scrapy.Request(results.get('paging').get('next'), callback=self.follower)

    def get_info(self, response,meta):
        item = {}
        item['name'] = response.css('.ProfileHeader-name::text').extract_first()
        item['sign'] = response.css('.RichText ProfileHeader-headline::text').extract_first()
        item['discribe'] = response.css('.ProfileHeader-info::text').extract()
        yield item
        followeeurl = 'https://www.zhihu.com/api/v4/members/'+meta['id']+'/followees?'
        followersurl = 'https://www.zhihu.com/api/v4/members/'+meta['id']+'/followers?'
        data = {
            'include': 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics',
            'offset': '0',
            'limit': '20',
        }
        data = urllib.parse.urlencode(data)
        followeeurl = followeeurl + data
        followerurl = followersurl + data
        yield scrapy.Request(followeeurl, callback=self.followee)
        yield scrapy.Request(followerurl, callback=self.followerurl)