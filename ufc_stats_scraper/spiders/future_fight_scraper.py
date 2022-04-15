from inspect import BoundArguments
import scrapy
import numpy as np
from ufc_stats_scraper.util import *


class UfcFutureFightSpider(scrapy.Spider):
    name = "ufc_future_fights"
    start_urls = ["http://ufcstats.com/statistics/events/upcoming?page=all"]

    def parse(self, response):
        future_event_links = response.css("a.b-link::attr(href)").getall()
        yield from response.follow_all(future_event_links, self.parse_future_events)

    def parse_future_events(self, response):
        future_matchups = response.css("a.b-link::attr(data-link)").getall()
        event_context = normalize_results(
            response.css("li.b-list__box-list-item::text").getall()
        )
        yield from response.follow_all(
            future_matchups,
            self.parse_future_matchups,
            cb_kwargs={"event_context": event_context},
        )

    def parse_future_matchups(self, response, event_context):
        date = event_context[0]
        location = event_context[1]
        fighter_names = normalize_results(
            response.css("a.b-fight-details__table-header-link::text").getall()
        )

        fighter_1 = fighter_names[0]
        fighter_2 = fighter_names[1]

        bout = normalize_results(
            response.css("i.b-fight-details__fight-title::text").getall()
        )[0]

        yield {
            "fighter_1": fighter_1,
            "fighter_2": fighter_2,
            "date": date,
            "bout": bout,
            "location": location,
        }
