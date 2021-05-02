import time

import scrapy
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from logzero import logfile, logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CountriesSpiderSpider(scrapy.Spider):
    # Initializing log file
    logfile("openaq_spider.log", maxBytes=1e6, backupCount=3)
    name = "countries_spider"
    allowed_domains = ["toscrape.com"]

    # Using a dummy website to start scrapy request
    def start_requests(self):
        url = "http://quotes.toscrape.com"
        yield scrapy.Request(url=url, callback=self.parse_countries)

    def parse_countries(self, response):
        # driver = webdriver.Chrome()  # To open a new browser window and navigate it

        # Use headless option to not open a new browser window
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome("/Users/ad/chromedriver")

        # Getting list of Countries
        driver.get("https://www.debate.org/opinions/do-you-agree-with-the-black-lives-matter-movement-1")

        while True:
            time.sleep(1)
            try:
                element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="col-wi"]/div/div[5]/a')))
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
