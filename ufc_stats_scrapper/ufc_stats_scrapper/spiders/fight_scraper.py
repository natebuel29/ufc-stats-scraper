import scrapy


class UfcFightSpider(scrapy.Spider):
    name = "ufc_fight"
    # response.css("table.b-fight-details__table tbody tr::attr(data-link)").getall()
    start_urls = [
        'http://ufcstats.com/event-details/1fac46d466abd5b8'
    ]

    def parse(self, response):
        fight_links = response.css(
            "table.b-fight-details__table tbody tr::attr(data-link)").getall()
        yield from response.follow_all(fight_links, self.parse_fights)

    def parse_fights(self, response):
        page = response.url.split("/")[-2]
        filename = f'fights-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
