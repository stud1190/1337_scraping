'''
This file contains functions to extract torrent data from 1337x torrent pages
'''

import unicodedata

from bs4 import BeautifulSoup

def parse_int(text: str):
    '''
    Returns integer by parsing the text, or `None` if it cannot be parsed. 
    '''
    try:
        return int(text)
    except ValueError:
        return None

def _q(response, attr, nest=''):
    query = f'//ul[@class="list"]/li[strong/text()="{attr}"]/span{nest}/text()'
    return response.xpath(query).get()

def extract_magnet(response):
    list_item = response.css('main.container div.row ul li')
    result = list_item.xpath(
        'a[contains(@href, "magnet:") and contains(text(), "Magnet Download")]/@href')
    if len(result) != 1:
        return None
    return result.get()

def image_urls(response):
    active_tab_pane = response.css('div#description.tab-pane.active')
    source_urls = active_tab_pane.xpath('p/a[descendant::img]/@href').getall()
    thumb_urls = active_tab_pane.xpath('p/a/img/@data-original').getall()
    return source_urls, thumb_urls

def parse_torrent_page(response):
    scr_urls, th_urls = image_urls(response)
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
        'category': _q(response, "Category"),
        'type': _q(response, "Type"),
        'language': _q(response, "Language"),
        'total_size': _q(response, "Total size"),
        'uploaded_by': _q(response, "Uploaded By", nest='/a'),
        'downloads': _q(response, "Downloads"),
        'last_checked': _q(response, "Last checked"),
        'date_uploaded': _q(response, "Date uploaded"),
        'seeders': parse_int(_q(response, 'Seeders')),
        'leechers': parse_int(_q(response, "Leechers")),
        'magnet': extract_magnet(response),
        'screenshot_urls': scr_urls,
        'screenshot_thumb_urls': th_urls,
        'description': description,
    }
