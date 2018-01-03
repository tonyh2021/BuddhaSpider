# -*- coding: utf-8 -*-

# Spider for 91 buddha
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


import scrapy
import logging
import random
from buddha_item import BuddhaItem
from utils.data_store import DataStore


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
            scrapy.Request(
                url=self.start_urls[0],
                callback=self.parse_next_page,
                dont_filter=True),
            ]

    def parse(self, response):
        logger.info("Buddha - Parse : %s" % (response.url))
        xpath_str = '//*[@class="listchannel"]/a[@target="blank"]/@href'
        for href in response.xpath(xpath_str).extract():
            logger.info("Request Detail: %s" % (href))
            # 查询是否重复
            viewkey = self._viewkey_from_url(href)
            ds = DataStore()
            exists = ds.buddha_exists(viewkey)
            ds.close()
            if exists:
                logger.warning("Ignore, View: %s exits" % (viewkey))
                continue
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
        buddha = BuddhaItem()
        try:
            name = response.xpath(
                '//div[@id="viewvideo-title"]/text()').extract()[0]
            name = "".join(name.split())
            logger.info("Buddha - Parse Detail: %s" % (name))
        except (ValueError, IndexError):
            logger.error(
                "Buddha - Parse Detail Error: %s,\n\
                 name parse error" % (response.url))
            name = ''
        buddha["name"] = name

        buddha["url"] = response.url

        viewkey = ''
        try:
            download_url = response.xpath(
                '//video[@id="vid"]/source/@src').extract()[0]
            download_url = "".join(download_url.split())
            logger.info("Buddha - Parse Detail: %s" % (download_url))
            viewkey = self._viewkey_from_url(download_url)
        except (ValueError, IndexError):
            logger.error(
                "Buddha - Parse Detail Error: %s,\n\
                 download_url parse error" % (response.url))
            download_url = ''
        buddha["download_url"] = download_url
        buddha["viewkey"] = viewkey

        try:
            duration = response.xpath(
                '//div[@class="boxPart"]/text()').extract()[1]
            duration = "".join(duration.split())
            logger.info("Buddha - Parse Detail: %s" % (duration))
        except (ValueError, IndexError):
            logger.error(
                "Buddha - Parse Detail Error: %s,\n\
                 duration parse error" % (response.url))
            duration = ''
        buddha["duration"] = duration

        try:
            points = response.xpath(
                '//div[@class="boxPart"]/text()').extract()[-1]
            points = "".join(points.split())
            logger.info("Buddha - Parse Detail: %s" % (points))
        except (ValueError, IndexError):
            logger.error(
                "Buddha - Parse Detail Error: %s,\n\
                 points parse error" % (response.url))
            points = ''
        buddha["points"] = points

        try:
            add_time = response.xpath(
                '//div[@id="videodetails-content"]/\
                span[@class="title"]/text()').extract()[0]
            add_time = "".join(add_time.split())
            logger.info("Buddha - Parse Detail: %s" % (add_time))
        except (ValueError, IndexError):
            logger.error(
                "Buddha - Parse Detail Error: %s,\n\
                 add_time parse error" % (response.url))
            add_time = ''
        buddha["add_time"] = add_time

        try:
            author = response.xpath(
                '//div[@id="videodetails-content"]/a/\
                span[@class="title"]/text()').extract()[0]
            author = "".join(author.split())
            logger.info("Buddha - Parse Detail: %s" % (author))
        except (ValueError, IndexError):
            logger.error(
                "Buddha - Parse Detail Error: %s,\n\
                 author parse error" % (response.url))
            author = ''
        buddha["author"] = author

        try:
            more = response.xpath(
                '//span[@class="more"]/text()').extract()[0]
            more = "".join("".join(more).split())
            # logger.info("Buddha - Parse Detail: %s" % (
            #         more))
        except (ValueError, IndexError):
            logger.error(
                "Buddha - Parse Detail Error: %s,\n\
                 more parse error" % (response.url))
            more = ''
        desc = more
        logger.info("Buddha - Parse Detail: %s" % (
                desc))
        buddha["desc"] = desc

        # logger.info("Buddha - Parse Detail: %s" % (buddha))
        yield buddha
        # filename = 'buddha_detail_%s.html' % int(time.time())
        # with open(filename, 'wb') as response_file:
        #     response_file.write(response.body)

    def parse_next_page(self, response):
        xpath_str = '//*[@id="paging"]/div/form/a/@href'
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

    def _viewkey_from_url(self, url):
        key = 'viewkey='
        viewkey = ''
        if key in url:
            start = url.index(key) + len(key)
            end = start + 20
            viewkey = url[start:end]
        return viewkey
