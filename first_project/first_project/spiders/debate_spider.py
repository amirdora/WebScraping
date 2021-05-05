import scrapy
from scrapy import Item


class DebateSpider(scrapy.Spider):
    name = 'crawl_arg'
    allowed_domains = ['debate.org']
    start_urls = [
        'https://www.debate.org/opinions/?sort=popular'
    ]

    def parse(self, response):
        self.logger.info('DebateSpider: A response from %s just arrived!', response.url)
        urls = get_all_urls(response)
        # iterating through 5 urls
        for url2 in urls[0:5]:
            concatenated_url = "https://www.debate.org" + url2
            self.logger.info('DebateSpider: Url %s', concatenated_url)
            item = QuotesbotItem()
            item['text'] = concatenated_url
            item['author'] = "author"
            item['tags'] = "tags"
            yield item

def get_all_urls(response):
    return response.css('a.a-image-contain::attr(href)').getall()


class QuotesbotItem(Item):
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
