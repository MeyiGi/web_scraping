import time
from playwright.sync_api import sync_playwright

def download_zillow_page(page, url):
    for i in range(3):
        response = page.goto(url, wait_until="domcontentloaded")
        if response.status == 404:
            return False
        
        if not page.title().startswith("60657"):
            print("Not recently sold")
            page.close()
            time.sleep(5)
            page = browser.new_page(java_script_enabled=True)
            continue
        
        print("Okay")
        target_element = page.query_selector("//div[@id=\"search-page-list-container\"]")
        
        for i in range(12):
            target_element.evaluate("element => element.scrollBy(0, 500)")
            time.sleep(0.5)
            
        time.sleep(2)
        with open(f"./html_exports/zillow_{city_name}-{state}-{zip_code}_{page_num}.html", "w", encoding="utf-8") as f:
            f.write(target_element.inner_html())
            
        print(f"Page {page_num} downloaded.")
        return True

playwright = sync_playwright().start()

browser = playwright.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])

city_name = "Chicago".replace(" ", "-")
state = "IL"
zip_code = "60657"

for page_num in range(1, 4):
    page = browser.new_page(java_script_enabled=True)
    url = f'https://www.zillow.com/{city_name}-{state}-{zip_code}/{page_num}_p'
    
    if not download_zillow_page(page, url):
        raise Exception("Page not found")
    
    page.close()
    time.sleep(3)

browser.close()
playwright.stop()