# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    company = scrapy.Field()
    team = scrapy.Field()
    job = scrapy.Field()
    salary = scrapy.Field()
    require = scrapy.Field()
    city = scrapy.Field()
