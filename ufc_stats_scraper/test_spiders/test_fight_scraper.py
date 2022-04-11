import unittest
from ufc_stats_scraper.spiders.fight_scraper import *
from scrapy import Selector


class TestUfcFightSpider(unittest.TestCase):
    def setUp(self):
        self.spider = UfcFightSpider()
        # self.fake_response = Selector()

    def test(self):
        print("did it work?")
        self.assertEqual(0, 0)
