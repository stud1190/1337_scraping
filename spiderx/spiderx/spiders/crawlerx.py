from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

import unicodedata

def parse_int(text: str):
    '''
    Returns integer by parsing the text, or None if it cannot be parsed. 
    '''
    try:
        return int(text)
    except ValueError:
        return None

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

    def Q(self, response, attr, nest=''):
        query = f'//ul[@class="list"]/li[strong/text()="{attr}"]/span{nest}/text()'
        return response.xpath(query).get()

    def extract_magnet(self, response):
        list_item = response.css('main.container div.row ul li')
        result = list_item.xpath(
            'a[contains(@href, "magnet:") and contains(text(), "Magnet Download")]/@href')
        if len(result) != 1:
            return None
        return result.get()

    def image_urls(self, response):
        active_tab_pane = response.css('div#description.tab-pane.active')
        source_urls = active_tab_pane.xpath('p/a[descendant::img]/@href').getall()
        thumb_urls = active_tab_pane.xpath('p/a/img/@data-original').getall()
        return source_urls, thumb_urls

    def parse_torrent(self, response):
        scr_urls, th_urls = self.image_urls(response)
        h1 = response.xpath('//h1/text()').get()
        if not str(h1).strip():
            return
        title = response.css('title::text').get().lstrip('Download ').rstrip('| 1337x')
        desc_node = response.css('#description').get()
        description = None
        if (desc_node is not None):
            plaintext = BeautifulSoup(desc_node, 'html.parser').get_text()
            description = unicodedata.normalize('NFKD', plaintext)

        yield {
            'page_url': response.url,
            'title': title,
            'category': self.Q(response, "Category"),
            'type': self.Q(response, "Type"),
            'language': self.Q(response, "Language"),
            'total_size': self.Q(response, "Total size"),
            'uploaded_by': self.Q(response, "Uploaded By", nest='/a'),
            'downloads': self.Q(response, "Downloads"),
            'last_checked': self.Q(response, "Last checked"),
            'date_uploaded': self.Q(response, "Date uploaded"),
            'seeders': parse_int(self.Q(response, 'Seeders')),
            'leechers': parse_int(self.Q(response, "Leechers")),
            'magnet': self.extract_magnet(response),
            'screenshot_urls': scr_urls,
            'screenshot_thumb_urls': th_urls,
            'description': description,
        }
