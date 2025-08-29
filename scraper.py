# scraper.py

import os
import random
from datetime import datetime
from dotenv import load_dotenv
from serpapi import SerpApiClient

def get_google_news_articles(themes, start_date, end_date, site_target, num_articles):
    """
    Performs a flexible Google News search based on provided criteria.

    Args:
        themes (list): Keywords or themes to search for.
        start_date (str): The start date in "YYYY-MM-DD" format.
        end_date (str): The end date in "YYYY-MM-DD" format.
        site_target (str): The specific website to search within.
        num_articles (int): The specific number of articles to fetch.

    Returns:
        list: A list of dictionaries representing the fetched articles.
    """
    load_dotenv()
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        print("CRITICAL FAILURE: SerpApi API key not found in .env file.")
        return []

    search_terms = " OR ".join([f'"{theme}"' for theme in themes])
    search_query = f"{search_terms} site:{site_target}"
    
    print(f"--- Scraper: Searching for {num_articles} articles with themes: {themes} ---")

    try:
        start_date_formatted = datetime.strptime(start_date, "%Y-%m-%d").strftime("%m/%d/%Y")
        end_date_formatted = datetime.strptime(end_date, "%Y-%m-%d").strftime("%m/%d/%Y")
        
        params = {
            "q": search_query,
            "engine": "google",
            "gl": "ke",
            "hl": "en",
            "tbm": "nws",
            "num": num_articles,
            "api_key": api_key,
            "tbs": f"cdr:1,cd_min:{start_date_formatted},cd_max:{end_date_formatted}"
        }
        
        client = SerpApiClient(params)
        results = client.get_dict()
        
    except Exception as e:
        print(f"Scraper: An error occurred while calling SerpApi for news. Error: {e}")
        return []

    if 'news_results' not in results or not results['news_results']:
        print("Scraper: API did not return any news articles for the specified criteria.")
        return []

    articles_list = [{'title': item.get('title'), 'link': item.get('link'), 'summary': item.get('snippet')}
                     for item in results['news_results']]

    print(f"--- Scraper: Successfully fetched {len(articles_list)} articles. ---")
    return articles_list

def get_relevant_image_url(theme):
    """
    Finds a relevant, high-quality, and DIRECT image URL, avoiding problematic sources.
    """
    print(f"Scraper: Searching for a relevant image for theme: '{theme}'...")
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        print("Scraper: SerpApi API key not found, cannot fetch image.")
        return None

    # A list of sources that are difficult to embed images from directly.
    BANNED_IMAGE_SOURCES = ["tiktok.com", "pinterest.com", "facebook.com", "instagram.com"]

    image_query = f"professional real estate {theme} kenya"

    try:
        params = {
            "q": image_query,
            "engine": "google_images",
            "ijn": "0",
            "api_key": api_key,
            "tbs": "isz:l,ic:color,itp:photo" # Filters: Large, Full Color, Photo
        }
        client = SerpApiClient(params)
        results = client.get_dict()

        if 'images_results' in results and results['images_results']:
            # Loop through the results to find a suitable, direct link.
            for image_data in results['images_results']:
                source_domain = image_data.get('source', '').lower()
                image_url = image_data.get('original', '')

                # Check 1: Is the source domain in our banned list?
                is_banned = any(banned_site in source_domain for banned_site in BANNED_IMAGE_SOURCES)
                if is_banned:
                    print(f"Scraper: Skipping banned source: {source_domain}")
                    continue # Skip to the next image in the loop

                # Check 2: Does the URL look like a direct link to an image file?
                if image_url.endswith(('.jpg', '.jpeg', '.png')):
                    print(f"Scraper: Successfully found valid image URL: {image_url}")
                    return image_url # Found a good one, return it and exit the function

            # If the loop finishes without finding a good URL from a valid source
            print("Scraper: Could not find a direct image link after checking results.")
            return None
        else:
            print("Scraper: No relevant images found.")
            return None
    except Exception as e:
        print(f"Scraper: An error occurred during image search. Error: {e}")
        return None