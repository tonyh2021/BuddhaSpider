# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BuddhaItem(scrapy.Item):
    name = scrapy.Field()            # 视频名称
    url = scrapy.Field()             # 视频 url
    download_url = scrapy.Field()    # 视频下载地址 url
    duration = scrapy.Field()        # 时长
    points = scrapy.Field()          # 积分
    add_time = scrapy.Field()        # 添加时间
    author = scrapy.Field()          # 作者
    desc = scrapy.Field()            # 描述
