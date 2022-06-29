import unittest
import os
from ufc_stats_scraper.spiders.future_fight_scraper import *
from scrapy import Selector


class TestUfcFutureFightSpider(unittest.TestCase):
    def setUp(self):
        self.spider = UfcFutureFightSpider()
        self.event_context = ["June, 2 2012", "test location"]

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
        self.assertEqual(results.pop("date"), "2012-06-02")
        self.assertEqual(results.pop("location"), "test location")
        self.assertEqual(results.pop("bout"), "UFC Lightweight Title Bout")
        self.assertEqual(results.pop("event_name"), "UFC 274: Oliveira vs. Gaethje")
        self.assertEqual(len(results), 0)
