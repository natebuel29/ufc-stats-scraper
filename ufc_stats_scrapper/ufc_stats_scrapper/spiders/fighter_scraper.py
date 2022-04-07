from os import stat
import scrapy
import numpy as np


class UfcFightSpider(scrapy.Spider):
    name = "ufc_fighter"
    start_urls = [
        'http://ufcstats.com/fighter-details/aec185309b4843d0'
    ]

    # def parse(self, response):
    #     alphabetized_fighter_links = response.css(
    #         "section div.b-statistics__nav-inner ul li a::attr(href)").getall()
    #     print(alphabetized_fighter_links)
    #     yield from response.follow_all(alphabetized_fighter_links, self.fetch_all_fighters)

    # def fetch_all_fighters(self, response):
    #     all_pages = response.css(
    #         "li.b-statistics__paginate-item a::attr(href)").getall()
    #     yield response.follow(all_pages[len(all_pages)-1], self.parse_fighters)

    # def parse_fighters(self, response):
    #     fighters = response.css(
    #         "section table.b-statistics__table tbody tr.b-statistics__table-row td.b-statistics__table-col a::attr(href)").getall()
    #     yield from response.follow_all(fighters, self.parse_fighter)

    def parse(self, response):
        name = str.strip(response.css(
            "section span.b-content__title-highlight ::text").get())
        nickname = str.strip(response.css(
            "p.b-content__Nickname ::text").get())
        first_name = name.split(" ")[0]
        last_name = name.split(" ")[1]

        record = str.strip(response.css(
            "span.b-content__title-record ::text").get()).split(" ")[1]

        fstats = response.css("li.b-list__box-list-item ::text").getall()
        fstats = self.strip_scrapped_data(fstats)
        print(fstats)

    def strip_scrapped_data(self, results):
        results = list(map(str.strip, results))
        while "" in results:
            results.remove("")
        return results
