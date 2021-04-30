import scrapy


class CrawlQuotesSpider(scrapy.Spider):
    name = "crawl_test"

    def start_requests(self):
        # predefinded pages to crawl
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            request = scrapy.Request(url=url, callback=self.parse_tag)
            request.meta['tag_name'] = url.split('/')[-1]
            yield request

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
