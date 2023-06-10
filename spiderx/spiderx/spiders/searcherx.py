'''
Usage: TODO
'''

import urllib.parse

import scrapy

from .extract import parse_torrent_page

def get_result_links(response):
    return response.css('td.name').xpath('a[starts-with(@href, "/torrent/")]/@href').getall()

class SearcherxSpider(scrapy.Spider):
    name = "searcherx"
    allowed_domains = ["1337x.to"]
    ## start url from page 1
    ## If response URL path starts with /search, then yield next search URL and
    ## all result page URLS
    ##
    ## Else, parse it using parse_torrent_page
    start_urls = ["https://1337x.to/"]

    def start_requests(self):
        search_term = (getattr(self, "query", None) or
            getattr(self, "search", None) or
            getattr(self, "q", None))
        if search_term is None:
            raise ValueError("No search query provided")
        encoded_term = urllib.parse.urlencode({'search': search_term})
        search_url = 'https://1337x.to/srch?' + encoded_term;
        yield scrapy.Request(search_url, self.parse)


    def parse_torrent_info(self, response):
        yield from parse_torrent_page(response)

    def parse(self, response):
        torrent_links = response.css('td.name').xpath('a[starts-with(@href, "/torrent/")]/@href')
        yield from response.follow_all(torrent_links, self.parse_torrent_info)

        pagination_links = response.css('div.pagination ul li a')
        yield from response.follow_all(pagination_links, self.parse)
