# _*_ coding: utf-8 _*_
__author__ = 'Tony'
__date__ = '2017/12/31 12:06'


import sys
import os
import argparse
from BuddhaSpider.utils.data_store import DataStore
from BuddhaSpider.spiders.buddha_spider import BuddhaSpider
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging


# 将系统当前目录设置为项目根目录
# os.path.abspath(__file__)为当前文件所在绝对路径
# os.path.dirname为文件所在目录
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def crawl():
    # 顺序执行 buddha 抓取命令，通过 type 来确认抓取类型
    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(BuddhaSpider, type=0)
        yield runner.crawl(BuddhaSpider, type=1)
        reactor.stop()
    crawl()
    # blocks process so always keep as the last statement
    reactor.run()


def query():
    ds = DataStore()
    urls = ds.fetch_download_url(100)
    with open('urls.txt', 'w') as f:
        f.write('\n')
    for url in urls:
        with open('urls.txt', 'a') as f:
            f.write('%s\n' % (url))
        print("%s" % (url))
    ds.close()


# Create ArgumentParser() object
parser = argparse.ArgumentParser()

# Add argument
parser.add_argument('-mode', type=int, help='seletc run mode.\n\
                        0: scrapy crawl buddha. \n\
                        1: query from sqlite')

# Parse argument
args = parser.parse_args()

if args.mode == 0:
    crawl()
elif args.mode == 1:
    query()
else:
    crawl()
