from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse

@dataclass
class Business:
    name: str = None
    address: str = None
    website: str = None
    phone_number: str = None
    reviews_count: int = None
    reviews_average: float = None
    
@dataclass
class BusinessList:
    business_list : list[Business] = field(default_factory=list)
    
    def dataframe(self):
        return pd.json_normalize((asdict(business) for business in self.business_list), sep="")

    def save_to_excel(self, filename):
        self.dataframe().to_excel(f"{filename}.xlsx", index=False)
        
    def save_to_csv(self, filename):
        self.dataframe().to_csv(f"{filename}.csv", index=False)
     
def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        page.goto("https://www.google.com/maps", timeout=60000)
        page.wait_for_timeout(5000)
        
        page.locator("//input[@id=\"searchboxinput\"]").fill(search_for)
        page.wait_for_timeout(3000)
        
        page.keyboard.press("Enter")
        page.wait_for_timeout(5000)
        
        listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()
        print(len(listings))
        
        business_list = BusinessList()
        
        for listing in listings[:5]:
            listing.click()
            page.wait_for_timeout(5000)
            
            name_xpath = '//h1[contains(@class, "fontHeadlineLarge")]'
            address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
            website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
            phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
            reviews_span_xpath = '//span[@role="img"]'

            business = Business()            
            if page.locator(name_xpath).count() > 0:
                business.name = page.locator(name_xpath).all()[0].inner_text()
            else:
                business.name = ""
            if page.locator(address_xpath).count() > 0:
                business.address = page.locator(address_xpath).all()[0].inner_text()
            else:
                business.address = ""
            if page.locator(website_xpath).count() > 0:
                business.website = page.locator(website_xpath).all()[0].inner_text()
            else:
                business.website = ""
            if page.locator(phone_number_xpath).count() > 0:
                business.phone_number = page.locator(phone_number_xpath).all()[0].inner_text()
            else:
                business.phone_number = ""
            if listing.locator(reviews_span_xpath).count() > 0:
                business.reviews_average = float(
                    listing.locator(reviews_span_xpath).all()[0]
                    .get_attribute("aria-label")
                    .split()[0]
                    .replace(",", ".")
                    .strip()
                )
                business.reviews_count = int(
                    listing.locator(reviews_span_xpath).all()[0]
                    .get_attribute("aria-label")
                    .split()[2]
                    .replace(',','')
                    .strip()
                )
            else:
                business.reviews_average = ""
                business.reviews_count = ""
                
            business_list.business_list.append(business)
            
        business_list.save_to_csv("google_maps_data")
        business_list.save_to_excel("google_maps_data")
        
        browser.close()     
   
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)
    parser.add_argument("-l", "--location", type=str)
    args = parser.parse_args()
    
    if args.location and args.search:
        search_for = f"{args.search}  {args.location}"
    else:
        search_for = "dentist new york"
        
    main()