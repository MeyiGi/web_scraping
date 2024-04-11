import scrapy
from bookscraper.items import BookItem
from random import randint

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css("article.product_pod")
        
        for book in books:
            relative_url = book.css("h3 a ::attr(href)").get()
            
            book_url = "https://books.toscrape.com/"
            if "catalogue/" not in relative_url:
                book_url += "catalogue/"
            book_url += relative_url
            
            yield response.follow(book_url, callback=self.parse_book_page)
            
        next_page = response.css("li.next a ::attr(href)").get()
        
        if next_page is not None:
            
            next_page_url = "https://books.toscrape.com/"
            if "catalogue/" not in next_page:
                next_page_url += "catalogue/"
            next_page_url += next_page
            
            yield response.follow(next_page_url, callback=self.parse)
            
    def parse_book_page(self, response):
        
        table = response.css("table tr")
        book_item = BookItem()
        
        book_item["url"]             = response.url
        book_item["title"]           = response.css(".product_main h1::text").get(),
        book_item["upc"]             = table[0].css("td::text").get(),
        book_item["product_type"]    = table[1].css("td::text").get(),
        book_item["price_excl_tax"]  = table[2].css("td::text").get(),
        book_item["price_incl_tax"]  = table[3].css("td::text").get(),
        book_item["tax"]             = table[4].css("td::text").get(),
        book_item["availability"]    = table[5].css("td::text").get(),
        book_item["num_reviews"]     = table[6].css("td::text").get(),
        book_item["stars"]           = response.css(".product_main p.star-rating").attrib["class"],
        book_item["category" ]       = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
        book_item["description"]     = response.xpath("//div[@class='product_description']/following-sibling::p/text()").get(),
        book_item["price"] = response.css("p.price_color::text").get()
        
        yield book_item