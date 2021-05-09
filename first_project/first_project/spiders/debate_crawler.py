import time

import scrapy
from scrapy import Item
from selenium import webdriver
from selenium.webdriver.common.by import By


class DebateSpider(scrapy.Spider):
    name = 'debate_crawler'
    allowed_domains = ['debate.org']
    start_urls = ['https://www.debate.org/opinions/?sort=popular']

    def parse(self, response):
        urls = get_all_urls(response)
        self.logger.info('DebateSpider: A response from %s just arrived!', response.url)

        # Use headless option to not open a new browser window
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome("../chromedriver")

        # iterating through 5 urls
        for url2 in urls[0:5]:
            # Use headless option to not open a new browser window
            concatinated_url = "https://www.debate.org" + url2
            driver.get(concatinated_url)

            while True:
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

            topic = driver.find_element_by_class_name('q-title').text
            category = driver.find_element_by_xpath('//*[@id="breadcrumb"]/a[3]').text

            mainJson = dict(topic=topic, category=category, pro_arguments=[], con_arguments=[])

            yes_arguments = driver.find_elements_by_xpath("//div[@class='arguments args-yes']/ul/li[@class='hasData']")
            no_arguments = driver.find_elements_by_xpath("//div[@class='arguments args-no']/ul/li[@class='hasData']")

            # main json dictionary
            mainJson = self.getYesArguments(driver, mainJson, yes_arguments)
            mainJson = self.getNoArguments(driver, mainJson, no_arguments)

            yield mainJson

        driver.quit()

    def getYesArguments(self, driver, mainJson, yes_arguments):
        count_yes = 1
        for x in yes_arguments:
            try:
                h2_path = "//div[@class='arguments args-yes']/ul/li[@class='hasData'][%s]/h2" % count_yes
                p_path = "//div[@class='arguments args-yes']/ul/li[@class='hasData'][%s]/p" % count_yes

                title = driver.find_element(By.XPATH, h2_path).text
                body = driver.find_element(By.XPATH, p_path).text

                count_yes = count_yes + 1
                self.logger.info('DebateSpider: count yes %s', count_yes)

                item = ArgumentItem()
                item['title'] = title
                item['body'] = body
                mainJson['pro_arguments'].append(item)

            except Exception:
                continue
        return mainJson

    def getNoArguments(self, driver, mainJson, yes_arguments):
        countNo = 1
        for x in yes_arguments:
            try:
                h2_path = "//div[@class='arguments args-no']/ul/li[@class='hasData'][%s]/h2" % countNo
                p_path = "//div[@class='arguments args-no']/ul/li[@class='hasData'][%s]/p" % countNo

                title = driver.find_element(By.XPATH, h2_path).text
                body = driver.find_element(By.XPATH, p_path).text

                countNo = countNo + 1
                self.logger.info('DebateSpider: count No %s', countNo)

                item = ArgumentItem()
                item['title'] = title
                item['body'] = body
                mainJson['con_arguments'].append(item)

            except Exception:
                continue
        return mainJson


class ArgumentItem(Item):
    title = scrapy.Field()
    body = scrapy.Field()


def get_all_urls(response):
    return response.css('a.a-image-contain::attr(href)').getall()
