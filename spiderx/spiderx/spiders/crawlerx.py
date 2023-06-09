from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CrawlerxSpider(CrawlSpider):
    '''
    ejfwaeif
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
        result = list_item.xpath('a[contains(@href, "magnet:") and contains(text(), "Magnet Download")]/@href')
        if len(result) != 1:
            return None
        return result.get();

    def image_urls(self, response):
        active_tab_pane = response.css('div#description.tab-pane.active')
        source_urls = active_tab_pane.xpath('p/a[descendant::img]/@href').getall()
        thumb_urls = active_tab_pane.xpath('p/a/img/@data-original').getall()
        return source_urls, thumb_urls

    def parse_torrent(self, response):
        scr_urls, th_urls = self.image_urls(response)
        yield {
            'page_url': response.url,
            'title': response.xpath('//h1/text()').get(),
            'category': self.Q(response, "Category"),
            'type': self.Q(response, "Type"),
            'language': self.Q(response, "Language"),
            'total_size': self.Q(response, "Total size"),
            'uploaded_by': self.Q(response, "Uploaded By", nest='/a'),
            'downloads': self.Q(response, "Downloads"),
            'last_checked': self.Q(response, "Last checked"),
            'date_uploaded': self.Q(response, "Date uploaded"),
            'seeders': self.Q(response, 'Seeders'),
            'leechers': self.Q(response, "Leechers"),
            'magnet': self.extract_magnet(response),
            'screenshot_source_urls': scr_urls,
            'screenshot_thumb_urls': th_urls,
            ## 'description': TODO
        }
