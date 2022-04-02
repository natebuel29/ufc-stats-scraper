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
        # stats_list = response.css(
        #     "section.b-fight-details__section table tbody td.b-fight-details__table-col p.b-fight-details__table-text::text").getall()
        stats_list = response.css(
            "tbody.b-fight-details__table-body td p ::text").getall()
        stats_list = list(map(str.strip, stats_list))
        # while '---' in stats_list:
        #     stats_list.remove('---')
        while "" in stats_list:
            stats_list.remove("")
        np_stats = np.array(stats_list)
        stats_matrix = np.reshape(np_stats, (57, 2))

        red_fighter = stats_matrix[0][0]
        blue_fighter = stats_matrix[0][1]
        rkd = int(stats_matrix[1][0])
        bkd = int(stats_matrix[1][1])
        rsigstrper = int(self.check_null(
            stats_matrix[3][0]).replace("%", ""))/100
        bsigstrper = int(self.check_null(
            stats_matrix[3][1]).replace("%", ""))/100
        rtotstrper = self.compute_percentage(stats_matrix[4][0])
        btotstrper = self.compute_percentage(stats_matrix[4][1])
        rtdper = int(self.check_null(stats_matrix[6][0]))
        btdper = int(self.check_null(stats_matrix[6][1]))
        rsubatt = int(self.check_null(stats_matrix[7][0]))
        bsubatt = int(self.check_null(stats_matrix[7][1]))
        rrev = int(self.check_null(stats_matrix[8][0]))
        brev = int(self.check_null(stats_matrix[8][1]))
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
        print(stats_matrix)

    def compute_percentage(self, stat):
        results = stat.split(" of ")
        if int(results[1]) == 0:
            return 0
        return round(int(results[0])/int(results[1]), 2)

    def check_null(self, stat):
        if stat == '---':
            return '0'
        else:
            return stat

    def convert_minutes_to_seconds(self, time):
        time_list = time.split(":")
        return int(time_list[0]) * 60 + int(time_list[1])

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


# -> returns fighter names response.css("section.b-fight-details__section table tbody td.b-fight-details__table-col p.b-fight-details__table-text a::text").getall()

# returns fighter stats -> response.css("section.b-fight-details__section table tbody td.b-fight-details__table-col p.b-fight-details__table-text::text").getall()
# will need to do the following things ->
# 1. strip the strings -> stripped_list = list(map(str.strip,test_list))
# 2. remove empty string and --- from list ->
# while '---' in stripped_list:stripped_list.remove('---')
# >>> while "" in stripped_list: stripped_list.remove("")
