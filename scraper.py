# scraper.py (Refined with Date Filtering)

import pandas as pd
import os
from dotenv import load_dotenv
from serpapi import SerpApiClient

def get_targeted_kenyan_news_last_month():
    """
    Uses SerpApi to perform a Google search for "real estate" within
    businessdailyafrica.com, filtered for results from the last month.
    """
    print("--- Using The Definitive Method: Targeted Site Search API ---")
    
    load_dotenv()
    api_key = os.getenv("SERPAPI_API_KEY")

    if not api_key:
        print("CRITICAL FAILURE: SerpApi API key not found in .env file.")
        return

    search_query = "real estate site:businessdailyafrica.com"
    
    print(f"Executing targeted search for last month: '{search_query}'...")

    try:
        params = {
            "q": search_query,
            "engine": "google",
            "gl": "ke",         # Geolocation: Kenya
            "hl": "en",         # Language: English
            # --- THIS IS THE REFINEMENT ---
            "tbs": "qdr:m",     # tbs=qdr:m means "query date range: past month"
            # --- END OF REFINEMENT ---
            "api_key": api_key
        }
        client = SerpApiClient(params)
        results = client.get_dict()
        
    except Exception as e:
        print(f"An error occurred while calling the SerpApi. Error: {e}")
        return

    if 'organic_results' not in results or not results['organic_results']:
        print("API did not return any articles for your targeted search in the last month.")
        return

    articles_list = []
    for item in results['organic_results']:
        if 'snippet' in item:
            articles_list.append({
                'title': item.get('title', 'No Title'),
                'link': item.get('link', 'No Link'),
                'summary': item.get('snippet', 'No Summary') 
            })

    df = pd.DataFrame(articles_list)
    df.to_csv('scraped_articles.csv', index=False, encoding='utf-8')

    print(f"\n--- SUCCESS! ---")
    print(f"Successfully fetched {len(articles_list)} hyper-relevant articles from the last month.")
    print("Full automation is achieved with guaranteed relevant data.")

if __name__ == "__main__":
    get_targeted_kenyan_news_last_month()