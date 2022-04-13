import scrapy
import numpy as np
from ufc_stats_scraper.util import *


class UfcFightSpider(scrapy.Spider):
    name = "ufc_fights"
    start_urls = ["http://ufcstats.com/statistics/events/completed?page=all"]

    def parse(self, response):
        fight_event_links = response.css(
            "table.b-statistics__table-events tbody tr.b-statistics__table-row i.b-statistics__table-content a::attr(href)"
        ).getall()
        yield from response.follow_all(fight_event_links, self.parse_fight_events)

    def parse_fight_events(self, response):
        fight_links = response.css(
            "table.b-fight-details__table tbody tr::attr(data-link)"
        ).getall()
        yield from response.follow_all(fight_links, self.parse_fight)

    def parse_fight(self, response):
        # red fighter data will always be in index 0 and blue fighter data will always be in index 1

        # scrap the fighter names
        fighter_results = self.normalize(
            response.css("section a.b-fight-details__person-link ::text").getall()
        )

        red_fighter = fighter_results[0]
        blue_fighter = fighter_results[1]

        # scrap the winner
        winner_results = normalize_results(
            response.css(
                "section div.b-fight-details__person i.b-fight-details__person-status ::text"
            ).getall()
        )

        r_win = 1 if winner_results[0] == "W" else 0
        b_win = 1 if winner_results[1] == "W" else 0

        # scrap fight details
        fdetails_results = normalize_results(
            response.css("section div.b-fight-details__fight ::text").getall()
        )

        wei_class = fdetails_results[0]
        method = fdetails_results[2]
        round_ = fdetails_results[4]
        time = fdetails_results[6]
        t_format = fdetails_results[8]
        ref = fdetails_results[10]
        details = str.strip(fdetails_results[12]) if len(fdetails_results) == 13 else ""

        # scrap fight statistics
        fstats_list = normalize_results(
            response.xpath('//table[@style="width: 745px"]//p/text()').getall()
        )

        np_stats = np.array(fstats_list)

        if np_stats.size == 34:
            # convert stats array to a 17 x 2 matrix
            stats_matrix = np.reshape(np_stats, (17, 2))
            r_kd = int(stats_matrix[0][0])
            b_kd = int(stats_matrix[0][1])
            r_sigstr = self.compute_percentage(stats_matrix[1][0])
            b_sigstr = self.compute_percentage(stats_matrix[1][1])
            r_totstr = self.compute_percentage(stats_matrix[3][0])
            b_totstr = self.compute_percentage(stats_matrix[3][1])
            r_td = int(self.null_check(stats_matrix[5][0]).replace("%", "")) / 100
            b_td = int(self.null_check(stats_matrix[5][1]).replace("%", "")) / 100
            r_sub = int(self.null_check(stats_matrix[6][0]))
            b_sub = int(self.null_check(stats_matrix[6][1]))
            r_rev = int(self.null_check(stats_matrix[7][0]))
            b_rev = int(self.null_check(stats_matrix[7][1]))
            r_ctrl = self.convert_minutes_to_seconds(stats_matrix[8][0])
            b_ctrl = self.convert_minutes_to_seconds(stats_matrix[8][1])
            r_hstr = self.compute_percentage(stats_matrix[11][0])
            b_hstr = self.compute_percentage(stats_matrix[11][1])
            r_bstr = self.compute_percentage(stats_matrix[12][0])
            b_bstr = self.compute_percentage(stats_matrix[12][1])
            r_lstr = self.compute_percentage(stats_matrix[13][0])
            b_lstr = self.compute_percentage(stats_matrix[13][1])
            r_dis = self.compute_percentage(stats_matrix[14][0])
            b_dis = self.compute_percentage(stats_matrix[14][1])
            r_cli = self.compute_percentage(stats_matrix[15][0])
            b_cli = self.compute_percentage(stats_matrix[15][1])
            r_gro = self.compute_percentage(stats_matrix[16][0])
            b_gro = self.compute_percentage(stats_matrix[16][1])

            yield {
                "r_fighter": red_fighter,
                "b_fighter": blue_fighter,
                "r_win": r_win,
                "b_win": b_win,
                "wei_class": wei_class,
                "method": method,
                "round": round_,
                "time": time,
                "t_format": t_format,
                "ref": ref,
                "details": details,
                "r_kd": r_kd,
                "b_kd": b_kd,
                "r_sigstr": r_sigstr,
                "b_sigstr": b_sigstr,
                "r_totstr": r_totstr,
                "b_totstr": b_totstr,
                "r_td": r_td,
                "b_td": b_td,
                "r_sub": r_sub,
                "b_sub": b_sub,
                "r_rev": r_rev,
                "b_rev": b_rev,
                "r_ctrl": r_ctrl,
                "b_ctrl": b_ctrl,
                "r_hstr": r_hstr,
                "b_hstr": b_hstr,
                "r_bstr": r_bstr,
                "b_bstr": b_bstr,
                "r_lstr": r_lstr,
                "b_lstr": b_lstr,
                "r_dis": r_dis,
                "b_dis": b_dis,
                "r_cli": r_cli,
                "b_cli": b_cli,
                "r_gro": r_gro,
                "b_gro": b_gro,
            }
        else:
            yield {
                "r_fighter": red_fighter,
                "b_fighter": blue_fighter,
                "r_win": r_win,
                "b_win": b_win,
                "wei_class": wei_class,
                "method": method,
                "round": round_,
                "time": time,
                "t_format": t_format,
                "ref": ref,
                "details": details,
            }

    def compute_percentage(self, stat):
        if "of" not in stat:
            return 0
        results = stat.split(" of ")
        if int(results[1]) == 0:
            return 0
        return round(int(results[0]) / int(results[1]), 2)

    def null_check(self, stat):
        if stat == "---" or stat == "--":
            return "0"
        else:
            return stat

    def convert_minutes_to_seconds(self, time):
        if ":" not in time:
            return 0
        else:
            time_list = time.split(":")
            return int(time_list[0]) * 60 + int(time_list[1])
