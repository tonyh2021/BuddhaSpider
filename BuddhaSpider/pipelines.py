# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import sqlite3
from utils import data_store
# from scrapy.exceptions import DropItem


class BuddhaPipeline(object):
    # item pipelines

    def process_item(self, item, spider):
        return item


class Sqlite3Pipeline(object):
    # save items to Sqlite3

    def __init__(self, db_file_name, db_table_name):
        self.db_file_name = db_file_name
        self.db_table_name = db_table_name
        self.ds = data_store.DataStore()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_file_name=crawler.settings.get('SQLITE3_FILE_NAME'),
            db_table_name=crawler.settings.get('SQLITE3_TABLE_NAME')
        )

    def open_spider(self, spider):
        self.conn = sqlite3.connect(self.db_file_name)
        self.cursor = self.conn.cursor()
        # self.cursor.execute(
        #     data_store.DROP_TABLE_CMD.format(tbl=self.db_table_name))
        self.cursor.execute(
            data_store.CREATE_TALE_CMD.format(tbl=self.db_table_name))

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        tal = self.db_table_name
        viewkey = item['viewkey']
        name = self.sqliteEscape(item['name'])
        url = item['url']
        download_url = item['download_url']   # 视频下载地址 url
        duration = self.sqliteEscape(item['duration'])        # 时长
        points = self.sqliteEscape(item['points'])          # 积分
        add_time = self.sqliteEscape(item['add_time'])        # 添加时间
        author = self.sqliteEscape(item['author'])         # 作者
        desc = self.sqliteEscape(item['desc'])            # 描述
        self.cursor.execute(data_store.INSERT_CMD.format(
            tbl=tal,
            viewkey=viewkey,
            name=name,
            url=url,
            download_url=download_url,
            duration=duration,
            points=points,
            add_time=add_time,
            author=author,
            desc=desc))
        self.conn.commit()
        return item

    def sqliteEscape(self, keyWord):
        keyWord = keyWord.replace("/", "//")
        keyWord = keyWord.replace("'", '"')
        keyWord = keyWord.replace("[", "/[")
        keyWord = keyWord.replace("]", "/]")
        keyWord = keyWord.replace("%", "/%")
        keyWord = keyWord.replace("&", "/&")
        keyWord = keyWord.replace("_", "/_")
        keyWord = keyWord.replace("(", "/(")
        keyWord = keyWord.replace(")", "/)")
        return keyWord
