import logging
from datetime import time

import scrapy
from logzero import logfile, logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


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
            # Use headless option to not open a new browser window
            options = webdriver.ChromeOptions()
            options.add_argument("headless")
            desired_capabilities = options.to_capabilities()
            driver = webdriver.Chrome("/Users/ad/chromedriver")
            # Getting list of Countries
            concatinated_url = "https://www.debate.org" + url2

            driver.get(concatinated_url)

            while True:
                try:
                    element = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="col-wi"]/div/div[5]/a')))
                    driver.execute_script("arguments[0].click();", element)

                except Exception:
                    break

            # Extracting country names
            args = driver.find_elements_by_xpath('//*[@id="yes-arguments"]/ul/li')

            countries_count = 0
            # Using Scrapy's yield to store output instead of explicitly writing to a JSON file
            for country in args:
                yield {
                    "country": country.text,
                }
                countries_count += 1

            driver.quit()
            logger.info(f"Total number of Countries in openaq.org: {countries_count}")
