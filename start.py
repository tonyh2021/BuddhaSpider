# _*_ coding: utf-8 _*_
__author__ = 'Tony'
__date__ = '2017/12/31 12:06'


from scrapy.cmdline import execute
import sys
import os
import argparse
from BuddhaSpider.utils.data_store import DataStore


# 将系统当前目录设置为项目根目录
# os.path.abspath(__file__)为当前文件所在绝对路径
# os.path.dirname为文件所在目录
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def crawl():
    # 执行 buddha 抓取命令
    # 执行命令，相当于在控制台cmd输入改名了
    execute("scrapy crawl buddha".split())


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
