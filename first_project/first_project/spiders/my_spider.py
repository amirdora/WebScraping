import logging
import time

import scrapy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


def get_all_urls(response):
    return response.xpath("//span[@class='image-frame']/a[1]/@href").extract()


def parseProArguments(item, yes_arguments):
    for argument in yes_arguments:
        title = argument.find_element_by_xpath('//h2').text
        body = argument.find_element_by_xpath('//p').text

        item['pro_arguments'].append({
            'title': title,
            'body': body})
    return item


def parseConArguments(item, no_arguments):
    for argument in no_arguments:
        title = argument.find_element_by_xpath('//h2').text
        body = argument.find_element_by_xpath('//p').text

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
        driver = self.initializingSileniumDriver()

        # iterating through 5 urls
        for url2 in urls[0:5]:
            # Use headless option to not open a new browser window
            # Getting list of Countries
            concatinated_url = "https://www.debate.org" + url2
            driver.get(concatinated_url)

            while True:
                time.sleep(1)
                try:
                    self.loadMoreData(driver)
                except Exception:
                    break

            # Extracting country names
            yes_arguments = driver.find_elements_by_xpath('//*[@id="yes-arguments"]/ul/li')
            no_arguments = driver.find_elements_by_xpath('//*[@id="no-arguments"]/ul/li')

            # main json dictionary
            item = dict(topic=driver.find_element_by_class_name('q-title').text,
                        category=driver.find_element_by_xpath('//*[@id="breadcrumb"]/a[2]').text,
                        pro_arguments=[],
                        con_arguments=[])

            item = parseProArguments(item, yes_arguments)

            item = parseConArguments(item, no_arguments)

            yield item
        driver.quit()

    def loadMoreData(self, driver):
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="col-wi"]/div/div[5]/a')))
        driver.execute_script("arguments[0].click();", element)

    def initializingSileniumDriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome("/Users/ad/chromedriver")
        return driver
