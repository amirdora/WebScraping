import scrapy


class CrawlDebatesSpider(scrapy.Spider):
    name = "crawl_debate"

    def start_requests(self):
        # predefinded pages to crawl

        self.getTopFiveOpinionUrls()

        #for url in urls:
         #   request = scrapy.Request(url=url, callback=self.parse_tag)
          #  request.meta['tag_name'] = url.split('/')[-1]
           # yield request

    def getTopFiveOpinionUrls(self):
        opinionUrls = "https://www.debate.org/opinions/?sort=popular";

        request = scrapy.Request(url=opinionUrls, callback=self.parse_urls)
        yield request

    def parse_urls(self, response):
        opinionList = response.css('#opinions-list')
        for opinion in opinionList:
            yield {
                'text': opinion
            }

    def parse_tag(self, response):

        # retrieve the tag name
        tag_name = response.meta['tag_name']

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
