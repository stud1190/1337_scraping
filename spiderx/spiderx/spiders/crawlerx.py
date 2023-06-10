'''
Crawl 1337X site and dump information about all available torrents
'''

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from .extract import parse_torrent_page

class CrawlerxSpider(CrawlSpider):
    '''
    Spider for crawling 1337x website
    '''
    name = "crawlerx"
    allowed_domains = ["1337x.to"]
    start_urls = ["https://1337x.to"]

    rules = (
        Rule(LinkExtractor(allow='/torrent/'), callback='parse_torrent', follow=True),
        Rule() ## Follow all links
    )

    def parse_torrent(self, response):
        return parse_torrent_page(response)
