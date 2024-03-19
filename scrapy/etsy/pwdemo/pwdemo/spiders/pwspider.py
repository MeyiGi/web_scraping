import scrapy
from pwdemo.itemloaders import ProductLoader
from pwdemo.items import ProductItem

class PwspiderSpider(scrapy.Spider):
    name = "pwspider"
    
    # custom_settings = {
    #     "FEEDS" : { "data/%(name)s_%(time)%.csv" : { "format" : "csv",} }}
    
    custom_settings = {
        "FEEDS" : { "data/%(name)s_%(time)s.csv" : { "format" : "csv",} }
    }
    
    def start_requests(self):
        start_url = "https://www.etsy.com/c/craft-supplies-and-tools?ref=homepage_shop_by_category_card"
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        product_links = response.css("div.js-merch-stash-check-listing")
        
        for product in product_links:
            product_url = product.css("a::attr(href)").get()
            yield response.follow(product_url, callback=self.parse_product)
        
        pagination_link = response.css(".wt-action-group__item")[-1]
        if pagination_link is not None:
            next_page = pagination_link.css("a::attr(href)").get()
            yield response.follow(next_page, callback=self.parse)
        
    def parse_product(self, response):
        
        product = ProductLoader(item=ProductItem(), selector=response)
        
        product.add_css("title", ".wt-text-body-01.wt-line-height-tight.wt-break-word.wt-mt-xs-1::text"),
        product.add_css("price", ".wt-text-title-larger.wt-mr-xs-1"),
        product.add_css("quantity_of_reviews", "h2.wt-mr-xs-2.wt-text-heading-small::text"),
        product.add_css("ratings", "span.wt-display-inline-block.wt-mr-xs-1 input::attr(value)"),
        
        if not product.get_output_value("quantity_of_reviews"):
            product.add_css(".wt-text-body-small::text").get()
            
        yield product.load_item()