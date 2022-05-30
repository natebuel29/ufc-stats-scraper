# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import mysql.connector

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class UfcFutureFightScraperPipeline:
    def __init__(self):
        host = os.environ.get("DB_HOST")
        user = os.environ.get("DB_USER")
        password = os.environ.get("DB_PASSWORD")
        database = os.environ.get("DB_DATABASE")
        if host != None and user != None and password != None and database != None:
            self.con = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
            )
            self.cur = self.con.cursor()
            self.create_table()
        else:
            self.con = None
            self.cur = None

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
        ##skip db steps if there is no connection
        if self.con != None:
            sql = """ INSERT IGNORE INTO future_fights (fighter_1,fighter_2,date_,bout,location_,event_name) VALUES (%s,%s,%s,%s,%s,%s)
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


class UfcFightScraperPipeline:
    def __init__(self):
        host = os.environ.get("DB_HOST")
        user = os.environ.get("DB_USER")
        password = os.environ.get("DB_PASSWORD")
        database = os.environ.get("DB_DATABASE")
        if host != None and user != None and password != None and database != None:
            self.con = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
            )
            self.cur = self.con.cursor()
            self.create_table()
        else:
            self.con = None
            self.cur = None

    def create_table(self):
        self.cur.execute(
            """CREATE TABLE if not exists fights(id INT AUTO_INCREMENT PRIMARY KEY,
            r_fighter TEXT,
            b_fighter TEXT,
            r_win INT,
            b_win INT,
            wei_class TEXT,
            method TEXT,
            round_ TEXT,
            time_ TEXT,
            t_format TEXT,
            ref TEXT,
            details TEXT,
            r_kd INT,
            b_kd INT,
            r_sigstr FLOAT,
            b_sigstr FLOAT,
            r_totstr FLOAT,
            b_totstr FLOAT,
            r_td INT,
            b_td INT,
            r_sub INT,
            b_sub INT,
            r_rev INT,
            b_rev INT,
            r_ctrl INT,
            b_ctrl INT,
            r_hstr FLOAT,
            b_hstr FLOAT,
            r_bstr FLOAT,
            b_bstr FLOAT,
            r_lstr FLOAT,
            b_lstr FLOAT,
            r_dis FLOAT,
            b_dis FLOAT,
            r_cli FLOAT,
            b_cli FLOAT,
            r_gro FLOAT,
            b_gro FLOAT)"""
        )

    def process_item(self, item, spider):
        ##skip db steps if there is no connection]
        if self.con != None:
            sql = """ INSERT IGNORE INTO fights (r_fighter,b_fighter,r_win,b_win,wei_class,method,round_,time_,t_format,ref,
            details,r_kd,b_kd,r_sigstr,b_sigstr,r_totstr,b_totstr,r_td,b_td,r_sub,b_sub,r_rev,b_rev,r_ctrl,b_ctrl,r_hstr,b_hstr,r_bstr,
            b_bstr,r_lstr,b_lstr,r_dis,b_dis,r_cli,b_cli,r_gro,b_gro) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            val = (
                item["r_fighter"],
                item["b_fighter"],
                item["r_win"],
                item["b_win"],
                item["wei_class"],
                item["method"],
                item["round"],
                item["time"],
                item["t_format"],
                item["ref"],
                item["details"],
                item["r_kd"],
                item["b_kd"],
                item["r_sigstr"],
                item["b_sigstr"],
                item["r_totstr"],
                item["b_totstr"],
                item["r_td"],
                item["b_td"],
                item["r_sub"],
                item["b_sub"],
                item["r_rev"],
                item["b_rev"],
                item["r_ctrl"],
                item["b_ctrl"],
                item["r_hstr"],
                item["b_hstr"],
                item["r_bstr"],
                item["b_bstr"],
                item["r_lstr"],
                item["b_lstr"],
                item["r_dis"],
                item["b_dis"],
                item["r_cli"],
                item["b_cli"],
                item["r_gro"],
                item["b_gro"],
            )

            self.cur.execute(sql, val)
            self.con.commit()

        return item


class UfcFighterScraperPipeline:
    def __init__(self):
        host = os.environ.get("DB_HOST")
        user = os.environ.get("DB_USER")
        password = os.environ.get("DB_PASSWORD")
        database = os.environ.get("DB_DATABASE")
        if host != None and user != None and password != None and database != None:
            self.con = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
            )
            self.cur = self.con.cursor()
            self.create_table()
        else:
            self.con = None
            self.cur = None

    def create_table(self):
        self.cur.execute(
            """CREATE TABLE if not exists fighters(id INT AUTO_INCREMENT PRIMARY KEY,
            name_ TEXT,
            nickname TEXT,
            f_name TEXT,
            l_name TEXT,
            wins INT,
            loses INT,
            ties INT,
            height INT,
            weight_ INT,
            reach INT,
            stance TEXT,
            dob TEXT,
            age INT,
            slpm FLOAT,
            str_ac FLOAT,
            sapm FLOAT,
            str_def FLOAT,
            td_avg FLOAT,
            td_acc FLOAT,
            td_def FLOAT,
            sub_avg FLOAT)"""
        )

    def process_item(self, item, spider):
        ##skip db steps if there is no connection
        if self.con != None:
            sql = """ INSERT INTO fighters (name_,nickname,f_name,l_name,wins,loses,ties,height,weight_,reach,stance,
            dob,age,slpm,str_ac,sapm,str_def,td_avg,td_acc,td_def,sub_avg) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            val = (
                item["name"],
                item["nickname"],
                item["f_name"],
                item["l_name"],
                item["wins"],
                item["loses"],
                item["ties"],
                item["height"],
                item["weight"],
                item["reach"],
                item["stance"],
                item["dob"],
                item["age"],
                item["slpm"],
                item["str_ac"],
                item["sapm"],
                item["str_def"],
                item["td_avg"],
                item["td_acc"],
                item["td_def"],
                item["sub_avg"],
            )

            self.cur.execute(sql, val)
            self.con.commit()

        return item
