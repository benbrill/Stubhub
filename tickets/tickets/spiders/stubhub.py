import scrapy
import re
from selenium import webdriver

class StubhubSpider(scrapy.Spider):
    name = "stubhub"

    start_urls = ["https://www.stubhub.com/los-angeles-dodgers-tickets/performer/1061/"]

    def __init__(self):
        self.driver = webdriver.Chrome(r'C:\WebDriver\bin\chromedriver.exe')

    def start_requests(self):
        self.driver.get("https://www.stubhub.com/los-angeles-dodgers-tickets/performer/1061/")

        while True:
            next = self.driver.find_element_by_css_selector(".formatted-link__button-as-link")

            try:
                next.click()

                # get the data and write it to scrapy items
            except:
                break

        self.driver.close()
        print("#" * 20)
        print(self.driver.page_source)
        return self.driver.page_source.encode('utf-8')

    def parse(self, response, **kwargs):
        
        for event in response.css('div.Panel.Panel-Border.EventItem'):
            event_name = event.css('.EventRedirection div::text').get()
            event_price = event.css('.AdvisoryPriceDisplay__content::text').get()

            yield {
                "name": event_name,
                "price": event_price
            }