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
        self.cursor.execute(
            data_store.DROP_TABLE_CMD.format(tbl=self.db_table_name))
        self.cursor.execute(
            data_store.CREATE_TALE_CMD.format(tbl=self.db_table_name))

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        tal = self.db_table_name
        name = item['name']
        url = item['url']
        self.cursor.execute(
            data_store.INSERT_CMD.format(tbl=tal, name=name, url=url))
        self.conn.commit()
        return item
