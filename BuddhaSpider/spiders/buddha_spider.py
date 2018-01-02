# -*- coding: utf-8 -*-

# Spider for 91 buddha
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


import scrapy
import logging
import random
from buddha_item import BuddhaItem
import time


logging.basicConfig(filename='buddha.log', level=logging.DEBUG, filemode='w')
logger = logging.getLogger(__name__)


class BuddhaSpider(scrapy.Spider):
    # BuddhaSpider

    name = "buddha"
    start_urls = ['http://91porn.com/v.php?viewtype=basic&category=rp']
    # http://91porn.com/v.php?viewtype=basic&category=rp&page=1 最近得分
    # http://91porn.com/v.php?viewtype=basic&category=rf 最近加精
    # start_urls = ['https://www.zhihu.com/signin']
    # start_urls = ['https://twitter.com/']
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": " application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 \
            Safari/537.36"
    }
    cookies = {
        "watch_times": "1"
    }

    def start_requests(self):
        return [
            scrapy.Request(
                url=self.start_urls[0],
                callback=self.parse),
            # scrapy.Request(
            #     url=self.start_urls[0],
            #     callback=self.parse_next_page,
            #     dont_filter=True),
            ]

    def parse(self, response):
        logger.info("Buddha - Parse : %s" % (response.url))
        xpath_str = '//*[@class="listchannel"]/a'
        for item in response.xpath(xpath_str):
            href = item.xpath('@href').extract()[0]
            logger.info("Request Detail: %s" % (href))
            random_ip = str(random.randint(0, 255)) + "." + \
                str(random.randint(0, 255)) + "." + \
                str(random.randint(0, 255)) + "." + \
                str(random.randint(0, 255))
            self.headers["X-Forwarded-For"] = random_ip
            yield scrapy.Request(
                url=href,
                headers=self.headers,
                cookies=self.cookies,
                callback=self.parse_detail)
        # filename = 'buddha.html'
        # with open(filename, 'wb') as response_file:
        #     response_file.write(response.body)

    def parse_detail(self, response):
        useraction = response.xpath('//div[@id="useraction"]')
        videodetails = response.xpath('//div[@id="videodetails"]')
        logger.info("useraction: %s" % (useraction))
        logger.info("videodetails: %s" % (videodetails))
        buddha = BuddhaItem()
        buddha["name"] = response.xpath(
            '//div[@id="viewvideo-title"]/text()').extract()[0].strip()
        buddha["url"] = response.url
        logger.info("Buddha - Parse Detail: %s" % (buddha))
        yield buddha
        filename = 'buddha_detail_%s.html' % int(time.time())
        with open(filename, 'wb') as response_file:
            response_file.write(response.body)

    def parse_next_page(self, response):
        xpath_str = '//*[@id="paging"]/div/form/a/@href'
        try:
            next_url = response.urljoin(
                response.xpath(xpath_str).extract()[-1])
            logger.info("Buddha - Parse Next Page : %s" % (next_url))
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
                dont_filter=True)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_next_page,
                dont_filter=True)
        except Exception:
            logger.info("Buddha - Parse Next Page Error: %s" % (Exception))
            return
