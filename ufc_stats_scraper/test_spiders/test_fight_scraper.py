import unittest
import os
from ufc_stats_scraper.spiders.fight_scraper import *
from scrapy import Selector


class TestUfcFightSpider(unittest.TestCase):
    def setUp(self):
        self.spider = UfcFightSpider()

    def test_average_ufc_fight_page(self):
        test_file = open(
            os.path.abspath(
                "ufc_stats_scraper/test_spiders/test_resources/standard_test_fight.html"
            ),
            "r",
        )
        self.fake_response = Selector(text=test_file.read())
        test_file.close()
        results = next(self.spider.parse_fight(response=self.fake_response))

        self.assertEqual(results.pop("r_fighter"), "Curtis Blaydes")
        self.assertEqual(results.pop("b_fighter"), "Chris Daukaus")
        self.assertEqual(results.pop("r_win"), 1)
        self.assertEqual(results.pop("b_win"), 0)
        self.assertEqual(results.pop("wei_class"), "Heavyweight Bout")
        self.assertEqual(results.pop("method"), "KO/TKO")
        self.assertEqual(results.pop("round"), "2")
        self.assertEqual(results.pop("time"), "0:17")
        self.assertEqual(results.pop("t_format"), "5 Rnd (5-5-5-5-5)")
        self.assertEqual(results.pop("ref"), "Herb Dean")
        self.assertEqual(results.pop("details"), "Punch to Head At Distance")
        self.assertEqual(results.pop("r_kd"), 1)
        self.assertEqual(results.pop("b_kd"), 0)
        self.assertEqual(results.pop("r_sigstr"), 0.48)
        self.assertEqual(results.pop("b_sigstr"), 0.34)
        self.assertEqual(results.pop("r_totstr"), 0.48)
        self.assertEqual(results.pop("b_totstr"), 0.34)
        self.assertEqual(results.pop("r_td"), 0)
        self.assertEqual(results.pop("b_td"), 0)
        self.assertEqual(results.pop("r_sub"), 0)
        self.assertEqual(results.pop("b_sub"), 0)
        self.assertEqual(results.pop("r_rev"), 0)
        self.assertEqual(results.pop("b_rev"), 0)
        self.assertEqual(results.pop("r_ctrl"), 3)
        self.assertEqual(results.pop("b_ctrl"), 0)
        self.assertEqual(results.pop("r_hstr"), 0.42)
        self.assertEqual(results.pop("b_hstr"), 0.33)
        self.assertEqual(results.pop("r_bstr"), 0.5)
        self.assertEqual(results.pop("b_bstr"), 0.5)
        self.assertEqual(results.pop("r_lstr"), 1)
        self.assertEqual(results.pop("b_lstr"), 0)
        self.assertEqual(results.pop("r_dis"), 0.44)
        self.assertEqual(results.pop("b_dis"), 0.34)
        self.assertEqual(results.pop("r_cli"), 0)
        self.assertEqual(results.pop("b_cli"), 0)
        self.assertEqual(results.pop("r_gro"), 0.67)
        self.assertEqual(results.pop("b_gro"), 0)
        self.assertEqual(len(results), 0)

    def test_unusual_ufc_fight_page(self):
        test_file = open(
            os.path.abspath(
                "ufc_stats_scraper/test_spiders/test_resources/unusual_test_fight.html"
            ),
            "r",
        )
        self.fake_response = Selector(text=test_file.read())
        test_file.close()
        results = next(self.spider.parse_fight(response=self.fake_response))

        self.assertEqual(results.pop("r_fighter"), "Tai Bowden")
        self.assertEqual(results.pop("b_fighter"), "Jack Nilson")
        self.assertEqual(results.pop("r_win"), 1)
        self.assertEqual(results.pop("b_win"), 0)
        self.assertEqual(results.pop("wei_class"), "Open Weight Bout")
        self.assertEqual(results.pop("method"), "KO/TKO")
        self.assertEqual(results.pop("round"), "1")
        self.assertEqual(results.pop("time"), "4:46")
        self.assertEqual(results.pop("t_format"), "1 Rnd + OT (12-3)")
        self.assertEqual(results.pop("ref"), "John McCarthy")
        self.assertEqual(
            results.pop("details"),
            "Headbutts to Head On Ground\n        Submission to Strikes",
        )
        self.assertEqual(results.pop("r_kd"), None)
        self.assertEqual(results.pop("b_kd"), None)
        self.assertEqual(results.pop("r_sigstr"), None)
        self.assertEqual(results.pop("b_sigstr"), None)
        self.assertEqual(results.pop("r_totstr"), None)
        self.assertEqual(results.pop("b_totstr"), None)
        self.assertEqual(results.pop("r_td"), None)
        self.assertEqual(results.pop("b_td"), None)
        self.assertEqual(results.pop("r_sub"), None)
        self.assertEqual(results.pop("b_sub"), None)
        self.assertEqual(results.pop("r_rev"), None)
        self.assertEqual(results.pop("b_rev"), None)
        self.assertEqual(results.pop("r_ctrl"), None)
        self.assertEqual(results.pop("b_ctrl"), None)
        self.assertEqual(results.pop("r_hstr"), None)
        self.assertEqual(results.pop("b_hstr"), None)
        self.assertEqual(results.pop("r_bstr"), None)
        self.assertEqual(results.pop("b_bstr"), None)
        self.assertEqual(results.pop("r_lstr"), None)
        self.assertEqual(results.pop("b_lstr"), None)
        self.assertEqual(results.pop("r_dis"), None)
        self.assertEqual(results.pop("b_dis"), None)
        self.assertEqual(results.pop("r_cli"), None)
        self.assertEqual(results.pop("b_cli"), None)
        self.assertEqual(results.pop("r_gro"), None)
        self.assertEqual(results.pop("b_gro"), None)
        self.assertEqual(len(results), 0)
