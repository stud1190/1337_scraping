import scrapy


class A1337xSpiderSpider(scrapy.Spider):
    name = "1337x_spider"
    allowed_domains = ["1337x.to"]
    start_urls = ["https://1337x.to/"]

    ## On spider startup
    ## Read list of pending items

    def parse(self, response):
        self.log(f'{response.body}')