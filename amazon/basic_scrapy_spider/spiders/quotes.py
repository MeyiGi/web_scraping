#  Drag quotes.py to your spiders where exists '__init__.py'

import scrapy

class AmazonSearchProductSpider(scrapy.Spider):
    name = "amazon_search_product"

    custom_settings = {
        'FEEDS': { 'data/%(name)s_%(time)s.json': { 'format': 'json',}}
    }

    def start_requests(self):
        keyword_list = ['ipad']
        for keyword in keyword_list:
            amazon_search_url = f'https://www.amazon.com/s?k={keyword}'
            yield scrapy.Request(url=amazon_search_url, callback=self.discover_product_urls)

    def discover_product_urls(self, response):
        
        ## Discover Product URLs
        search_products = response.css("div.puis-card-border")
        for product in search_products:
            relative_url = product.css("h2 a::attr('href')").get()
            product_url = 'https://www.amazon.com' + relative_url
            yield scrapy.Request(url=product_url, callback=self.parse_product_data)
            
        ## Get All Pages
        pagination = response.css(".s-pagination-separator a::attr('href')").get()
        if pagination is not None:
            next_page_url = "https://www.amazon.com/" + pagination
            return scrapy.Request(url=next_page_url, callback=self.discover_product_urls)


    def parse_product_data(self, response):
        # Image extracting it is hard, especially In amazon,and there won’t be many tasks to extract images, etc.
        # In my view VARIANT is junk data,so I deleted it
        
        name            = response.css("#productTitle::text").get("").strip()
        price           = response.css('.a-price span[aria-hidden="true"] ::text').get("")
        stars           = response.css("i[data-hook=average-star-rating] ::text").get("").strip(),
        rating_count    = response.css("div[data-hook=total-review-count] ::text").get("").strip(),
        feature_bullets = [bullet.strip() for bullet in response.css("#feature-bullets li ::text").getall()]
        
        if not price:
            price = response.css('.a-price .a-offscreen ::text').get("")
        yield {
            "name": name,
            "price": price,
            "stars": stars,
            "rating_count": rating_count,
            "feature_bullets": feature_bullets,
        }