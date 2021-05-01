import logging

import scrapy


class CrawlDebatesSpider(scrapy.Spider):
    name = "crawl_debate"

    def start_requests(self):
        urls = [
            'https://www.debate.org/opinions/?sort=popular',
        ]
        for url in urls:
            requestUrl = scrapy.Request(url=url, callback=self.parse_urls)
            requestUrl.meta['tag_name'] = url.split('/')[-1]
            yield requestUrl

    def parse_urls(self, response):
        global items
        urls = response.xpath("//span[@class='image-frame']/a[1]/@href").extract()
        for url2 in urls[0:5]:
            concatinated_url = "https://debate.org" + url2
            requestData = scrapy.Request(url=concatinated_url, callback=self.parse_tag)
            requestData.meta['tag_name2'] = url2.split('/')[-1]
            yield requestData

    def parse_tag(self, response):

        # retrieve the tag name
        tag_name = response.meta['tag_name2']

        # use css function to parse the html and find the tags that contains the arguments
        yes_arguments = response.css('#yes-arguments .hasData')
        no_arguments = response.css('#no-arguments .hasData')

        # main json dictionary
        item = dict(topic=response.css('.q-title::text').get(),
                    category=response.css('#breadcrumb a::text')[1].get(),
                    pro_arguments=[],
                    con_arguments=[])

        item = self.parseProArguments(item, yes_arguments)

        item = self.parseConArguments(item, no_arguments)

        yield item

    def parseProArguments(self, item, yes_arguments):
        for quote_html_tag in yes_arguments:
            title = quote_html_tag.css('h2 ::text').get()
            body = quote_html_tag.css('p ::text').getall()

            item['pro_arguments'].append({
                'title': title,
                'body': body})
        return item

    def parseConArguments(self, item, no_arguments):
        for quote_html_tag in no_arguments:
            title = quote_html_tag.css('h2 ::text').get()
            body = quote_html_tag.css('p ::text').getall()

            item['con_arguments'].append({
                'title': title,
                'body': body})
        return item
