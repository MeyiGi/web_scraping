import scrapy
import json


class LinkedinCompanySpider(scrapy.Spider):
    name = "linkedin_company_profile"

    #add your own list of company urls here
    company_pages = [
        'https://www.linkedin.com/company/usebraintrust?trk=public_jobs_jserp-result_job-search-card-subtitle',
        'https://www.linkedin.com/company/centraprise?trk=public_jobs_jserp-result_job-search-card-subtitle'
    ]
    
    def start_requests(self):
        
        company_index_tracker = 0

        first_url = self.company_pages[company_index_tracker]

        yield scrapy.Request(url=first_url, callback=self.parse_company_profile, meta={'company_index_tracker': company_index_tracker})

        
                             
    def parse_company_profile(self, response):
        company_index_tracker = response.meta["company_index_tracker"]
        
        company_item = {}
        
        company_item["name"] = response.css('.top-card-layout__entity-info h1::text').get(default='not-found').strip()
        company_item["summary"] = response.css('.top-card-layout__entity-info h4 span::text').get(default='not-found').strip()
        
        try:
            company_details = response.css(".core-section-container__content .mb-2")
            
            company_industry_line = company_details[1].css(".text-md::text").getall()
            company_item["industry"] = company_industry_line[1].strip()
            
            company_size_line = company_details[2].css('.text-md::text').getall()
            company_item["size"] = company_size_line[1].strip()
            
            company_size_line = company_details[5].css(".text-md::text").getall()
            company_item["founded"] = company_size_line[1].strip()
            
            
        except IndexError:
            print("Error: Skipped Company - Some details missing")
            
        yield company_item
            
        company_index_tracker += 1
        
        if company_index_tracker <= len(self.company_pages) - 1:
            next_url = self.company_pages[company_index_tracker]
            
            yield scrapy.Request(url=next_url, callback=self.parse_company_profile, meta={"company_index_tracker" : company_index_tracker})
            
    def readRulFromJobsFile(self):
        res = []
        
        with open("jobs.json") as file:
            jobs = json.load(file)
            
            for job in jobs:
                if job["company_link"] != "not_found":
                    self.company_pages.append(job["company_link"])
                    
        self.company_pages = list(set(self.company_pages))