# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class UfcStatsScraperPipeline:
    connection = {
        "host": "uu141odqvz2rnrv.cdxfj1ghajls.us-east-1.rds.amazonaws.com",
        "username": "mysqlAdmin",
        "password": "HTIJCGxO4=huACd-qPjYJBznoGWUmG",
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

    def process_item(self, item, spider):
        print(f"yo this is the item {item} ")
        return item
