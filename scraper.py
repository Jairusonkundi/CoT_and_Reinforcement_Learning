# scraper.py (The Definitive, API-Based Solution - With Correct Query)

import requests
import pandas as pd
import os
from dotenv import load_dotenv

def get_news_from_api_final():
    """
    Fetches news articles related to Kenyan real estate using the GNews API
    with a query that is compatible with the free plan.
    """
    print("--- Using The Professional Method: GNews API ---")
    
    load_dotenv()
    api_key = os.getenv("GNEWS_API_KEY")

    if not api_key:
        print("CRITICAL FAILURE: GNews API key not found in .env file.")
        return

    # --- THIS IS THE FINAL FIX ---
    # We use a simpler query without the "AND" operator, which is a paid feature.
    # This search will find articles that contain both "kenya" and "real estate".
    query = "kenya real estate"
    # --- END OF FIX ---
    
    URL = f"https://gnews.io/api/v4/search?q={query}&lang=en&token={api_key}"
    
    print(f"Fetching data from GNews API with a valid query...")

    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()
        
    except requests.RequestException as e:
        print(f"Failed to fetch data from the API. Error: {e}")
        # GNews often sends error details inside the JSON response
        print(f"API Response: {response.text}")
        return

    if 'articles' not in data or not data['articles']:
        print("API did not return any articles for the query. This may be due to a lack of recent news on the topic.")
        return

    articles_list = []
    for item in data['articles']:
        articles_list.append({
            'title': item.get('title', 'No Title'),
            'link': item.get('url', 'No Link'),
            'summary': item.get('description', 'No Summary') 
        })

    df = pd.DataFrame(articles_list)
    df.to_csv('scraped_articles.csv', index=False, encoding='utf-8')

    print(f"\n--- SUCCESS! ---")
    print(f"Successfully fetched {len(articles_list)} articles using the GNews API.")
    print("Full automation is achieved. Your project is complete.")

if __name__ == "__main__":
    get_news_from_api_final()