import unittest
import os
from ufc_stats_scraper.spiders.fighter_scraper import *
from scrapy import Selector


class TestUfcFighterSpider(unittest.TestCase):
    def setUp(self):
        self.spider = UfcFighterSpider()

    def test_average_ufc_fighter_page(self):
        test_file = open(
            os.path.abspath(
                "ufc_stats_scraper/test_spiders/test_resources/standard_test_fighter.html"
            ),
            "r",
        )
        self.fake_response = Selector(text=test_file.read())
        test_file.close()
        results = next(self.spider.parse_fighter(response=self.fake_response))
        self.assertEqual(results.pop("name"), "Israel Adesanya")
        self.assertEqual(results.pop("nickname"), "The Last Stylebender")
        self.assertEqual(results.pop("f_name"), "Israel")
        self.assertEqual(results.pop("l_name"), "Adesanya")
        self.assertEqual(results.pop("wins"), 22)
        self.assertEqual(results.pop("loses"), 1)
        self.assertEqual(results.pop("ties"), 0)
        self.assertEqual(results.pop("height"), 76)
        self.assertEqual(results.pop("weight"), 185)
        self.assertEqual(results.pop("reach"), 80)
        self.assertEqual(results.pop("stance"), "Switch")
        self.assertEqual(results.pop("dob"), "Jul 22, 1989")
        self.assertEqual(results.pop("age"), 32)
        self.assertEqual(results.pop("slpm"), 3.84)
        self.assertEqual(results.pop("str_ac"), 0.49)
        self.assertEqual(results.pop("sapm"), 2.56)
        self.assertEqual(results.pop("str_def"), 0.61)
        self.assertEqual(results.pop("td_avg"), 0)
        self.assertEqual(results.pop("td_acc"), 0)
        self.assertEqual(results.pop("td_def"), 0.77)
        self.assertEqual(results.pop("sub_avg"), 0.2)
        self.assertEqual(len(results), 0)

    def test_unusual_ufc_fighter_page(self):
        test_file = open(
            os.path.abspath(
                "ufc_stats_scraper/test_spiders/test_resources/unusual_test_fighter.html"
            ),
            "r",
        )
        self.fake_response = Selector(text=test_file.read())
        test_file.close()
        results = next(self.spider.parse_fighter(response=self.fake_response))
        self.assertEqual(results.pop("name"), "Lowell Anderson")
        self.assertEqual(results.pop("nickname"), "")
        self.assertEqual(results.pop("f_name"), "Lowell")
        self.assertEqual(results.pop("l_name"), "Anderson")
        self.assertEqual(results.pop("wins"), 0)
        self.assertEqual(results.pop("loses"), 1)
        self.assertEqual(results.pop("ties"), 0)
        self.assertEqual(results.pop("height"), 66)
        self.assertEqual(results.pop("weight"), 160)
        self.assertEqual(results.pop("reach"), None)
        self.assertEqual(results.pop("stance"), "Orthodox")
        self.assertEqual(results.pop("dob"), None)
        self.assertEqual(results.pop("age"), None)
        self.assertEqual(results.pop("slpm"), 0)
        self.assertEqual(results.pop("str_ac"), 0)
        self.assertEqual(results.pop("sapm"), 0)
        self.assertEqual(results.pop("str_def"), 0)
        self.assertEqual(results.pop("td_avg"), 0)
        self.assertEqual(results.pop("td_acc"), 0)
        self.assertEqual(results.pop("td_def"), 0)
        self.assertEqual(results.pop("sub_avg"), 0)
        self.assertEqual(len(results), 0)
