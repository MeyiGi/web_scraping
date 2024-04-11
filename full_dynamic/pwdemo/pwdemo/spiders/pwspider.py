import scrapy
from scrapy_playwright.page import PageMethod

class PwspiderSpider(scrapy.Spider):
    name = "pwspider"

    def start_requests(self):
        start_url = "https://shoppable-campaign-demo.netlify.app"
        yield scrapy.Request(url=start_url, meta=dict(
            playwright=True,
            playwright_include_page=True,
            playwright_page_methods=[
                PageMethod("wait_for_selector", '.card-body'),
            ],
        ))

    async def parse(self, response):
        page = response.meta["playwright_page"]

        products = response.css(".card-body")
        
        item = {}
        for product in products:
            item["title"] = product.css(".card-title").get()
            item["description"] = product.css("p").get()
            item["price"] = product.css("label").get()
            
            print(item)
            
            yield item