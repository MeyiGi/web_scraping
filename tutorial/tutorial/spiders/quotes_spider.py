import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]
    
    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("span small::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }
            
        pagination_link = response.css("li.next a")
        yield from response.follow_all(pagination_link, callback=self.parse)
    
class AuthorSpider(scrapy.Spider):
    name = "author"
    start_urls = ["https://quotes.toscrape.com/"]
    
    def parse(self, response):
        author_page_link = response.css(".author + a")
        yield from response.follow_all(author_page_link, callback=self.parse_author)
        
        pagination_link = response.css("li.next a")
        yield from response.follow_all(pagination_link, callback=self.parse)
        
    def parse_author(self, response):
        yield {
            "name": response.css("h3.author-title::text").get(),
            "birthday": response.css("span.author-born-date::text").get(),
            "bio": response.css("div.author-description::text").get()
        }
    