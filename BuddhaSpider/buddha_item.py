# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BuddhaItem(scrapy.Item):
    name = scrapy.Field()            # 书名
    url = scrapy.Field()             # url
