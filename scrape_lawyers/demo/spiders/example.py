import scrapy


class ExampleSpider(scrapy.Spider):
    name = "example"
    start_url = "https://www.avvo.com/personal-injury-lawyer/ca.html?page=1"
    
    custom_settings = {
        "FEEDS" : {"data/%(name)s_%(time)s.csv" : {"format" : "csv"}}
    }

    def start_requests(self):
        start_url = "https://www.avvo.com/personal-injury-lawyer/ca.html?page=1"
        yield scrapy.Request(url=start_url, callback=self.parse)
        
    def parse(self, response):
        lawyer_urls = response.css(".search-result-lawyer-name::attr(href)")
        
        for lawyer_url in lawyer_urls:
            yield response.follow(lawyer_url, callback=self.parse_lawyer)
            
        pagination_link = response.css(".next a")
        if pagination_link is not None:
            next_page = pagination_link.css("a::attr(href)").get()
            yield response.follow(next_page, callback=self.parse)
            
    def parse_lawyer(self, response):
        item = {}
        
        address = response.xpath("//div[@class='contact-address']/div")
        
        item["fullname"] = response.css(".lawyer-name span::text").get()
        item["company_name"] = response.css(".contact-firm::text").get()
        item["website"] = response.css(".ga-click-website a::attr(href)").get()
        
        item["location"] = address.xpath('string(.)').get()
        # item["street_address"] = response.css('div[class="contact-address"] div:nth-child(3)::text').get()
        # item["raw_location"] = response.css('div[class="contact-address"] div:nth-child(3)::attr("data")').get()
        # item["city"] = loc_raw[0]
        # item["state"] = loc_raw[1]
        # item["zipcode"] = loc_raw[2]
        
        item["phone"] = response.css('.overridable-lawyer-phone-copy').get()

        yield item