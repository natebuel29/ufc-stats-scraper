import unittest
import os
from ufc_stats_scraper.spiders.future_fight_scraper import *
from scrapy import Selector


class TestUfcFutureFightSpider(unittest.TestCase):
    def setUp(self):
        self.spider = UfcFutureFightSpider()
        self.event_context = ["test date", "test location"]

    def test_standard_ufc_future_fight_page(self):
        test_file = open(
            os.path.abspath(
                "ufc_stats_scraper/test_spiders/test_resources/standard_test_future_fight.html"
            ),
            "r",
        )
        self.fake_response = Selector(
            text=test_file.read(),
        )
        test_file.close()
        results = next(
            self.spider.parse_future_matchups(
                response=self.fake_response, event_context=self.event_context
            )
        )
        self.assertEqual(results.pop("fighter_1"), "Charles Oliveira")
        self.assertEqual(results.pop("fighter_2"), "Justin Gaethje")
        self.assertEqual(results.pop("date"), "test date")
        self.assertEqual(results.pop("location"), "test location")
        self.assertEqual(results.pop("bout"), "UFC Lightweight Title Bout")
        self.assertEqual(len(results), 0)
