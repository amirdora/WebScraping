import logging
import time

import scrapy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


def get_all_urls(response):
    return response.xpath("//span[@class='image-frame']/a[1]/@href").extract()


def parseProArguments(driver, item, yes_arguments):
    count_yes = 1
    for argument in yes_arguments:
        h2_path = "//div[@class='arguments args-yes']/ul/li[@class='hasData'][%s]/h2" % count_yes
        p_path = "//div[@class='arguments args-yes']/ul/li[@class='hasData'][%s]/p" % count_yes

        title = driver.find_element(By.XPATH, h2_path).text
        body = driver.find_element(By.XPATH, p_path).text
        count_yes = count_yes + 1
        item['pro_arguments'].append({
            'title': title,
            'body': body})
    return item


def parseConArguments(driver, item, no_arguments):
    countNo = 1
    for argument in no_arguments:
        h2_path = "//div[@class='arguments args-no']/ul/li[@class='hasData'][%s]/h2" % countNo
        p_path = "//div[@class='arguments args-no']/ul/li[@class='hasData'][%s]/p" % countNo

        title = driver.find_element(By.XPATH, h2_path).text
        body = driver.find_element(By.XPATH, p_path).text
        countNo = countNo + 1

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
                self.logger.info("DebateSpider: while loop")
                try:
                    time.sleep(1)
                    element = driver.find_element_by_class_name('debate-more-btn')
                    if element.is_displayed():
                        self.logger.info('DebateSpider: button  %s', "true")
                        driver.execute_script("document.getElementsByClassName('debate-more-btn')[0].click()")
                    else:
                        self.logger.info('DebateSpider: button %s', "false")
                        break

                except Exception:
                    break

            # Extracting country names
            yes_arguments = driver.find_elements_by_xpath("//div[@class='arguments args-yes']/ul/li[@class='hasData']")
            no_arguments = driver.find_elements_by_xpath("//div[@class='arguments args-no']/ul/li[@class='hasData']")
            topic = driver.find_element_by_class_name('q-title').text
            category = driver.find_element_by_xpath('//*[@id="breadcrumb"]/a[3]').text
            # main json dictionary
            item = dict(topic=topic, category=category, pro_arguments=[], con_arguments=[])

            item = parseProArguments(driver, item, yes_arguments)

            item = parseConArguments(driver, item, no_arguments)

        yield item
        driver.quit()

    def initializingSileniumDriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome("../chromedriver")
        return driver
