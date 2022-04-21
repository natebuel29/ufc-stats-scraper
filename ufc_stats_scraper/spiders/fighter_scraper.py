import scrapy
import numpy as np

from ufc_stats_scraper.util import *


class UfcFighterSpider(scrapy.Spider):
    name = "ufc_fighters"
    start_urls = ["http://ufcstats.com/statistics/fighters?char=a&page=all"]

    def parse(self, response):
        alphabetized_fighter_links = response.css(
            "section div.b-statistics__nav-inner ul li a::attr(href)"
        ).getall()
        yield from response.follow_all(
            alphabetized_fighter_links, self.fetch_all_fighters
        )

    def fetch_all_fighters(self, response):
        all_pages = response.css(
            "li.b-statistics__paginate-item a::attr(href)"
        ).getall()
        yield response.follow(all_pages[len(all_pages) - 1], self.parse_fighters)

    def parse_fighters(self, response):
        fighters = response.css(
            "section table.b-statistics__table tbody tr.b-statistics__table-row td.b-statistics__table-col a::attr(href)"
        ).getall()
        yield from response.follow_all(fighters, self.parse_fighter)

    def parse_fighter(self, response):
        # scrap fighter name
        name = str.strip(
            response.css("section span.b-content__title-highlight ::text").get()
        )
        nickname = str.strip(response.css("p.b-content__Nickname ::text").get())
        first_name = name.split(" ")[0]
        last_name = name.split(" ")[1] if len(name.split(" ")) > 1 else "N/A"

        # scrap fighter record
        record_array = (
            str.strip(response.css("span.b-content__title-record ::text").get())
            .split(" ")[1]
            .split("-")
        )
        wins = int(record_array[0])
        loses = int(record_array[1])
        ties = int(record_array[2])

        # scrap fighter stats
        fstats = response.css("li.b-list__box-list-item ::text").getall()
        fstats = normalize_results(fstats)
        fstats = np.array(fstats)
        if fstats.size == 25:
            fstats = np.insert(fstats, 7, "---")
        stats_matrix = np.reshape(fstats, (13, 2))
        height = (
            convert_feet_to_inches(stats_matrix[0][1])
            if stats_matrix[0][1] != "---" and stats_matrix[0][1] != "--"
            else "N/A"
        )
        weight = (
            int(stats_matrix[1][1].split(" lbs.")[0])
            if stats_matrix[1][1] != "---" and stats_matrix[1][1] != "--"
            else "N/A"
        )
        reach = (
            int(stats_matrix[2][1].split('"')[0])
            if stats_matrix[2][1] != "---" and stats_matrix[2][1] != "--"
            else "N/A"
        )
        stance = (
            stats_matrix[3][1]
            if stats_matrix[3][1] != "---" and stats_matrix[3][1] != "--"
            else "N/A"
        )
        dob = (
            stats_matrix[4][1]
            if stats_matrix[4][1] != "---" and stats_matrix[4][1] != "--"
            else "N/A"
        )
        age = compute_age(dob) if dob != "N/A" else "N/A"
        slpm = (
            float(stats_matrix[5][1])
            if stats_matrix[5][1] != "---" and stats_matrix[5][1] != "--"
            else "N/A"
        )
        str_ac = (
            int(stats_matrix[6][1].replace("%", "")) / 100
            if stats_matrix[6][1] != "---" and stats_matrix[6][1] != "--"
            else "N/A"
        )
        sapm = (
            float(stats_matrix[7][1])
            if stats_matrix[7][1] != "---" and stats_matrix[7][1] != "--"
            else "N/A"
        )
        str_def = (
            int(stats_matrix[8][1].replace("%", "")) / 100
            if stats_matrix[8][1] != "---" and stats_matrix[8][1] != "--"
            else "N/A"
        )
        td_avg = (
            float(stats_matrix[9][1])
            if stats_matrix[9][1] != "---" and stats_matrix[9][1] != "--"
            else "N/A"
        )
        td_acc = (
            int(stats_matrix[10][1].replace("%", "")) / 100
            if stats_matrix[10][1] != "---" and stats_matrix[10][1] != "--"
            else "N/A"
        )
        td_def = (
            int(stats_matrix[11][1].replace("%", "")) / 100
            if stats_matrix[11][1] != "---" and stats_matrix[11][1] != "--"
            else "N/A"
        )
        sub_avg = (
            float(stats_matrix[12][1])
            if stats_matrix[12][1] != "---" and stats_matrix[12][1] != "--"
            else "N/A"
        )

        yield {
            "name": name,
            "nickname": nickname,
            "f_name": first_name,
            "l_name": last_name,
            "wins": wins,
            "loses": loses,
            "ties": ties,
            "height": height,
            "weight": weight,
            "reach": reach,
            "stance": stance,
            "dob": dob,
            "age": age,
            "slpm": slpm,
            "str_ac": str_ac,
            "sapm": sapm,
            "str_def": str_def,
            "td_avg": td_avg,
            "td_acc": td_acc,
            "td_def": td_def,
            "sub_avg": sub_avg,
        }
