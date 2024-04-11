import scrapy
from scrapy_playwright.page import PageMethod


scrolling_script = """
    const scrolls = 8
    let scrollCount = 0
    
    // scroll down and then wait for 0.5s
    const scrollInterval = setInterval(() => {
      window.scrollTo(0, document.body.scrollHeight)
      scrollCount++
    
      if (scrollCount === numScrolls) {
        clearInterval(scrollInterval)
      }
    }, 500)
"""


class ScrapingClubSpider(scrapy.Spider):
    name = "scraping_club"
    allowed_domains = ["scrapingclub.com"]
    
    def start_requests(self):
        url = "https://scrapingclub.com/exercise/list_infinite_scroll/"
        yield scrapy.Request(url, 
                             
        meta = {
            "playwright": True,
            "playwright_page_methods" : [
                PageMethod("evaluate", scrolling_script),
                PageMethod("wait_for_selector", ".post:nth-child(60)")
            ]
        })
        
    def parse(self, response):
        for product in response.css(".post"):
            # scrape product data
            url = product.css("a").attrib["href"]
            image = product.css(".card-img-top").attrib["src"]
            name = product.css("h4 a::text").get()
            price = product.css("h5::text").get()
    
            # add the data to the list of scraped items
            yield {
                "url": url,
                "image": image,
                "name": name,
                "price": price
            }
