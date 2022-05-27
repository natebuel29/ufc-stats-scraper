# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class UfcStatsScraperPipeline:
    connection = {
        "host": "uuz525xubt27v.cdxfj1ghajls.us-east-1.rds.amazonaws.com",
        "username": "mysqlAdmin",
        "password": "pjc-NMz12H.Roq=WTW^DwuxNoNGs02",
        "db": "thisisatest",
    }

    def __init__(self):
        self.con = mysql.connector.connect(
            host=self.connection["host"],
            user=self.connection["username"],
            password=self.connection["password"],
            database=self.connection["db"],
        )
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute(
            """CREATE TABLE if not exists future_fights(id INT AUTO_INCREMENT PRIMARY KEY,
            fighter_1 TEXT,
            fighter_2 TEXT,
            date_ TEXT,
            bout TEXT,
            location_ TEXT,
            event_name TEXT)"""
        )

    def process_item(self, item, spider):
        sql = """ INSERT OR IGNORE INTO future_fights (fighter_1,fighter_2,date_,bout,location_,event_name) VALUES (%s,%s,%s,%s,%s,%s)
        """
        val = (
            item["fighter_1"],
            item["fighter_2"],
            item["date"],
            item["bout"],
            item["location"],
            item["event_name"],
        )

        self.cur.execute(sql, val)
        self.con.commit()
        return item
