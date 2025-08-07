# scraper.py (Final Version - Using Local Manual Driver)

import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
# We no longer need webdriver_manager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin

def scrape_reuters_with_local_driver():
    """
    Scrapes Reuters using MS Edge and a manually downloaded driver to bypass
    all firewall and network issues.
    """
    query = "kenya+real+estate"
    URL = f"https://www.reuters.com/site-search/?query={query}"
    
    print("--- Using Final Method: Local Manual Driver ---")
    print(f"Accessing: {URL}")

    edge_options = Options()
    edge_options.add_argument("--window-size=1920,1080")
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # --- THIS IS THE FINAL FIX ---
    # We tell Selenium the exact path to the driver you downloaded.
    # Since it's in the same folder as the script, we just use its name.
    service = Service(executable_path="msedgedriver.exe")
    # --- END OF FIX ---
    
    driver = webdriver.Edge(service=service, options=edge_options)

    html_content = ""
    try:
        driver.get(URL)
        print("MS Edge browser is open. Looking for the cookie consent button...")

        try:
            wait = WebDriverWait(driver, 15)
            cookie_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            cookie_button.click()
            print("Cookie consent button clicked successfully.")
        except Exception:
            print("Cookie button not found or needed. Continuing...")

        time.sleep(3)
        html_content = driver.page_source
        print("Page content captured.")
    finally:
        driver.quit()
        print("Browser closed.")

    if not html_content:
        print("Failed to get HTML content.")
        return

    soup = BeautifulSoup(html_content, 'html.parser')
    articles = []
    
    results_container = soup.find('div', {'data-testid': 'search-results'})
    
    if not results_container:
        print("\nCRITICAL FAILURE: The page loaded but the content was not found.")
        return

    for item in results_container.find_all('li'):
        title_element = item.find('a', {'data-testid': 'Heading'})
        summary_element = item.find('p', {'data-testid': 'Body'})

        if title_element and summary_element:
            relative_link = title_element['href']
            full_link = urljoin("https://www.reuters.com", relative_link)
            title = title_element.get_text(strip=True)
            summary = summary_element.get_text(strip=True)
            articles.append({'title': title, 'link': full_link, 'summary': summary})

    if not articles:
        print("Scraping failed. Found results container, but it was empty.")
        return

    df = pd.DataFrame(articles)
    df.to_csv('scraped_articles.csv', index=False, encoding='utf-8')

    print(f"\n--- SUCCESS! ---")
    print(f"You have successfully scraped {len(articles)} articles.")
    print("All roadblocks are cleared. You can now complete your project.")

if __name__ == "__main__":
    scrape_reuters_with_local_driver()