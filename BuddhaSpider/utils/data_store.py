# -*- coding: utf-8 -*-

# sqlite utils for the project


import sqlite3
import settings as settings
import logging
import sys
import pandas as pd


# 创建一个日志器logger并设置其日志级别为DEBUG
logger = logging.getLogger(__name__)
# 创建一个流处理器handler并设置其日志级别为DEBUG
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

# 创建一个格式器formatter并将其添加到处理器handler
formatter = logging.Formatter(
    "[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s")
handler.setFormatter(formatter)

# 为日志器logger添加上面创建的处理器handler
logger.addHandler(handler)

SELECT_VIEWKEY_CMD = """SELECT viewkey FROM {tbl} WHERE viewkey
                        = '{viewkey}';"""
INSERT_CMD = """INSERT INTO {tbl} (
                    viewkey,
                    name,
                    url,
                    download_url,
                    image_url,
                    duration,
                    points,
                    add_time,
                    author,
                    desc) VALUES (
                        '{viewkey}',
                        '{name}',
                        '{url}',
                        '{download_url}',
                        '{image_url}',
                        '{duration}',
                        '{points}',
                        '{add_time}',
                        '{author}',
                        '{desc}');"""
DROP_TABLE_CMD = """DROP TABLE IF EXISTS {tbl};"""
CREATE_TALE_CMD = """CREATE TABLE IF NOT EXISTS {tbl} (
                    id integer primary key,
                    viewkey text,
                    name text,
                    url  text,
                    download_url  text,
                    image_url  text,
                    duration  text,
                    points  text,
                    add_time  text,
                    author  text,
                    desc text);"""


class DataStore(object):
    # utils class

    def __init__(self, reset=False):
        self.db_file_name = settings.SQLITE3_FILE_NAME
        self.db_table_name = settings.SQLITE3_TABLE_NAME
        self.conn = sqlite3.connect(self.db_file_name)
        self.cursor = self.conn.cursor()
        # Delete old records
        if not reset:
            return
        logger.info('Reset table: %s' % (self.db_table_name))
        self.cursor.execute(DROP_TABLE_CMD.format(tbl=self.db_table_name))
        self.cursor.execute(
            CREATE_TALE_CMD.format(tbl=self.db_table_name))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def buddha_exists(self, viewkey):
        query = SELECT_VIEWKEY_CMD.format(
            tbl=self.db_table_name, viewkey=viewkey)
        self.cursor.execute(query)
        viewkeys = self.cursor.fetchall()
        if len(viewkeys) > 0:
            return True
        return False

    def fetch_all(self):
        query = "SELECT * FROM {tbl}".format(tbl=self.db_table_name)
        df = pd.read_sql_query(query, self.conn)
        logger.info("\n %s " % (df))

    def fetch_download_url(self, limit=10):
        query = "SELECT download_url FROM {tbl} LIMIT {limit}".format(
            tbl=self.db_table_name, limit=limit)
        self.cursor.execute(query)
        urls = []
        for row in self.cursor:
            urls.append(row)
        return urls


def main():
    ds = DataStore()
    ds.close()


if __name__ == '__main__':
    main()
