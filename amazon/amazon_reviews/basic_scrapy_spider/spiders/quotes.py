import scrapy
from urllib.parse import urljoin


class AmazonReviewsSpider(scrapy.Spider):
    name = 'pwdemo'


    def start_requests(self):
        asin_list = ['B09G9GLLRN']
        for asin in asin_list:
            amazon_reviews_url = f"https://www.amazon.com/product-reviews/{asin}/"
            yield scrapy.Request(url=amazon_reviews_url, callback=self.parse_reviews, meta={"asin" : asin})
        
    def parse_reviews(self, response):
        asin = response.meta["asin"]
        next_page = response.css(".a-pagination .a-last>a::attr(href)").get()
        
        if next_page is not None:
            next_page = urljoin("https://www.amazon.com/", next_page)
            yield scrapy.Request(url=next_page, callback=self.parse_reviews, meta={"asin" : asin})
            
        review_elements = response.css("#cm_cr-review_list div.review")
        for review_element in review_elements:
            yield {
                "asin"  : asin,
                "text"  : review_element.css("span[data-hook=review-body] span::text").get(),
                "title" : review_element.css("a[data-hook=review-title] span::text").get(),
                "locating_and_date" : review_element.css("span[data-hook=review-date]::text").get()[-1],
                "ratings" : review_element.css("i[data-hook=review-star-rating] > span::text").get()
            }