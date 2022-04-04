import scrapy
import numpy as np


class UfcFightSpider(scrapy.Spider):
    name = "ufc_fight"
    # response.css("table.b-fight-details__table tbody tr::attr(data-link)").getall()
    # response.css("table.b-statistics__table-events tbody tr.b-statistics__table-row i.b-statistics__table-content a::attr(href)").getall()
    # start_urls = [
    #     'http://ufcstats.com/statistics/events/completed?page=all'
    # ]

    # look into scrappy items
    start_urls = [
        'http://ufcstats.com/fight-details/c4e866d9dd606faa'
    ]

    rf_index = 0
    bf_index = 1

    def parse(self, response):
        stats_list = response.css(
            "tbody.b-fight-details__table-body td p ::text").getall()
        stats_list = self.normalize_results(stats_list)
        winner_results = response.css(
            "section div.b-fight-details__person i.b-fight-details__person-status ::text").getall()
        winner_results = self.normalize_results(winner_results)
        fdetails_results = response.css(
            "section div.b-fight-details__fight ::text").getall()
        fdetails_results = self.normalize_results(fdetails_results)
        np_fdetails = np.array(fdetails_results)
        print(fdetails_results)
        np_stats = np.array(stats_list + winner_results)
        stats_matrix = np.reshape(np_stats, (58, 2))
        red_fighter = stats_matrix[0][0]
        blue_fighter = stats_matrix[0][1]
        rkd = int(stats_matrix[1][0])
        bkd = int(stats_matrix[1][1])
        rsigstrper = int(self.null_checlk(
            stats_matrix[3][0]).replace("%", ""))/100
        bsigstrper = int(self.null_checlk(
            stats_matrix[3][1]).replace("%", ""))/100

        wei_class = np_fdetails[0]
        method = np_fdetails[2]
        round_ = np_fdetails[4]
        time = np_fdetails[6]
        t_format = np_fdetails[8]
        ref = np_fdetails[9]
        details = np_fdetails[12]
        print(f"wei class is {wei_class}")
        print(f"method is {method}")
        print(f"round_ is {round_}")
        print(f"time is {time}")
        print(f"t_format is {t_format}")
        print(f"ref is {ref}")
        print(f"details is {details}")

        rtotstrper = self.compute_percentage(stats_matrix[4][0])
        btotstrper = self.compute_percentage(stats_matrix[4][1])
        rtdper = int(self.null_checlk(stats_matrix[6][0]))
        btdper = int(self.null_checlk(stats_matrix[6][1]))
        rsubatt = int(self.null_checlk(stats_matrix[7][0]))
        bsubatt = int(self.null_checlk(stats_matrix[7][1]))
        rrev = int(self.null_checlk(stats_matrix[8][0]))
        brev = int(self.null_checlk(stats_matrix[8][1]))
        rctrl = self.convert_minutes_to_seconds(stats_matrix[9][0])
        bctrl = self.convert_minutes_to_seconds(stats_matrix[9][1])
        rhstrper = self.compute_percentage(stats_matrix[33][0])
        bhstrper = self.compute_percentage(stats_matrix[33][1])
        rbstrper = self.compute_percentage(stats_matrix[34][0])
        bbstrper = self.compute_percentage(stats_matrix[34][1])
        rlstrper = self.compute_percentage(stats_matrix[35][0])
        blstrper = self.compute_percentage(stats_matrix[35][1])
        rdper = self.compute_percentage(stats_matrix[36][0])
        bdper = self.compute_percentage(stats_matrix[36][1])
        rclper = self.compute_percentage(stats_matrix[37][0])
        bclper = self.compute_percentage(stats_matrix[37][1])
        rgrdper = self.compute_percentage(stats_matrix[38][0])
        bgrdper = self.compute_percentage(stats_matrix[38][1])
        rwin = 1 if stats_matrix[57][0] == 'W' else 0
        bwin = 1 if stats_matrix[57][1] == 'W' else 0

        print(f"red fighter is {red_fighter}")
        print(f"blue fighter is {blue_fighter}")
        print(f"rkd is {rkd}")
        print(f"bkd is {bkd}")
        print(f"rsigstrper is {rsigstrper}")
        print(f"bsigstrper is {bsigstrper}")
        print(f"rtotstrper is {rtotstrper}")
        print(f"btotstrper is {btotstrper}")
        print(f"rtdper is {rtdper}")
        print(f"btdper is {btdper}")
        print(f"rsubatt is {rsubatt}")
        print(f"bsubatt is {bsubatt}")
        print(f"rrev is {rrev}")
        print(f"brev is {brev}")
        print(f"rctrl is {rctrl}")
        print(f"bctrl is {bctrl}")
        print(f"rhstrper is {rhstrper}")
        print(f"bhstrper is {bhstrper}")
        print(f"rbstrper is {rbstrper}")
        print(f"bbstrper is {bbstrper}")
        print(f"rlstrper is {rlstrper}")
        print(f"blstrper is {blstrper}")
        print(f"rdper is {rdper}")
        print(f"bdper is {bdper}")
        print(f"rclper is {rclper}")
        print(f"bclper is {bclper}")
        print(f"rgrdper is {rgrdper}")
        print(f"bgrdper is {bgrdper}")
        print(f"rwin is {rwin}")
        print(f"bwin is {bwin}")
        print(stats_matrix)

    def compute_percentage(self, stat):
        results = stat.split(" of ")
        if int(results[1]) == 0:
            return 0
        return round(int(results[0])/int(results[1]), 2)

    def null_checlk(self, stat):
        if stat == '---':
            return '0'
        else:
            return stat

    def strip_scrapped_data(self, results):
        list(map(str.strip, results))
        while "" in results:
            results.remove("")

        return results

    def convert_minutes_to_seconds(self, time):
        time_list = time.split(":")
        return int(time_list[0]) * 60 + int(time_list[1])

    def normalize_results(self, results):
        normalize_list = list(map(str.strip, results))
        while "" in normalize_list:
            normalize_list.remove("")
        return normalize_list

    # def parse(self, response):
    #     fight_event_links = response.css(
    #         "table.b-statistics__table-events tbody tr.b-statistics__table-row i.b-statistics__table-content a::attr(href)").getall()
    #     yield from response.follow_all(fight_event_links, self.parse_fight_events)

    # def parse_fight_events(self, response):
    #     fight_links = response.css(
    #         "table.b-fight-details__table tbody tr::attr(data-link)").getall()
    #     yield from response.follow_all(fight_links, self.parse_fight_events)

    # def parse_fight_event(self, response):
    #     page = response.url.split("/")[-2]
    #     filename = f'fights-{page}.html'
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log(f'Saved file {filename}')
