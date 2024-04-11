from urllib.parse import urlencode
import scrapy 
from chocolateScraper.items import ChocolateProduct 
from chocolateScraper.itemloaders import ChocolateProductLoader

API_KEY = "6921f3f8-6375-4e1d-9d07-b376c1da8d5e"

def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


class ChocolatespiderSpider(scrapy.Spider):

    name = 'chocolatesSpider'

    def start_requests(self):
        start_url = 'https://www.chocolate.co.uk/collections/all'
        yield scrapy.Request(url=get_proxy_url(start_url), callback=self.parse)

    def parse(self, response):

        products  = response.css('product-item')
        for product in products:
            chocolate = ChocolateProductLoader(item=ChocolateProduct(), selector=product)
            chocolate.add_css('name', "a.product-item-meta__title::text"),
            chocolate.add_css('price', 'span.price', re='<span class="price">\n              <span class="visually-hidden">Sale price</span>(.*)</span>'),
            chocolate.add_css('url', 'div.product-item-meta a::attr(href)')
            yield chocolate.load_item()
            
        next_page = response.css('[rel="next"] ::attr(href)').get()

        if next_page is not None:
            next_page_url = 'https://www.chocolate.co.uk' + next_page
            yield response.follow(get_proxy_url(next_page_url), callback=self.parse)