import logging

import scrapy


def get_all_urls(response):
    return response.xpath("//span[@class='image-frame']/a[1]/@href").extract()


def parseProArguments(item, yes_arguments):
    for quote_html_tag in yes_arguments:
        title = quote_html_tag.css('h2 ::text').get()
        body = quote_html_tag.css('p ::text').getall()

        item['pro_arguments'].append({
            'title': title,
            'body': body})
    return item


def parseConArguments(item, no_arguments):
    for quote_html_tag in no_arguments:
        title = quote_html_tag.css('h2 ::text').get()
        body = quote_html_tag.css('p ::text').getall()

        item['con_arguments'].append({
            'title': title,
            'body': body})
    return item


class CrawlDebatesSpider(scrapy.Spider):
    name = "crawl_debate"

    def start_requests(self):
        popularPageUrl = "https://www.debate.org/opinions/?sort=popular"
        requestUrl = scrapy.Request(url=popularPageUrl, callback=self.parse_urls)
        yield requestUrl

    def parse_urls(self, response):
        urls = get_all_urls(response)
        # iterating through 5 urls
        for url2 in urls[0:5]:
            concatinated_url = "https://debate.org" + url2
            requestData = scrapy.Request(url=concatinated_url, callback=self.parse_tag)
            yield requestData

    def parse_tag(self, response):

        # finding tags that contains the arguments
        yes_arguments = response.css('#yes-arguments .hasData')
        no_arguments = response.css('#no-arguments .hasData')

        # main json dictionary
        item = dict(topic=response.css('.q-title::text').get(),
                    category=response.css('#breadcrumb a::text')[1].get(),
                    pro_arguments=[],
                    con_arguments=[])

        item = parseProArguments(item, yes_arguments)

        item = parseConArguments(item, no_arguments)

        yield item
