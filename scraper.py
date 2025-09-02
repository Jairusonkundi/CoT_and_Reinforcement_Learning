# scraper.py
from serpapi import GoogleSearch
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

def _format_date(date_str):
    """
    Accepts YYYY-MM-DD and returns MM/DD/YYYY for SerpApi/GSearch tbs filter.
    """
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%m/%d/%Y")

def get_google_news_articles(themes, start_date, end_date, site_target=None, per_theme_limit=20):
    """
    Performs Google News searches for each theme and collects articles.
    Falls back to organic_results when needed and returns all collected articles.
    """
    if not SERPAPI_API_KEY:
        print("  -> [ERROR] Scraper: SerpApi API key not found. Set SERPAPI_API_KEY in .env")
        return []

    all_articles = []
    start_date_formatted = _format_date(start_date)
    end_date_formatted = _format_date(end_date)

    if not themes:
        print("  -> [INFO] Scraper: No themes provided to search.")
        return []

    for theme in themes:
        query = f'"{theme}"' if " " in theme else theme
        if site_target:
            query += f" site:{site_target}"

        print(f"  -> Scraper: Searching articles for theme: '{theme}' ...")
        params = {
            "engine": "google_news",   # preferred for news_results
            "q": query,
            "gl": "ke",
            "hl": "en",
            "api_key": SERPAPI_API_KEY,
            "num": per_theme_limit,
            "tbs": f"cdr:1,cd_min:{start_date_formatted},cd_max:{end_date_formatted}"
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()
        except Exception as e:
            print(f"  -> [ERROR] Scraper: API call failed for theme '{theme}'. Error: {e}")
            continue

        # Prefer news_results but fallback to organic_results (search page with tbm=nws may populate organic_results)
        articles = results.get("news_results") or results.get("organic_results") or []
        if not articles:
            print(f"  -> [INFO] Scraper: No results for theme '{theme}'.")
            continue

        for a in articles:
            title = a.get("title") or a.get("headline") or ""
            link = a.get("link") or a.get("source") or ""
            summary = a.get("snippet") or a.get("summary") or title
            # Only include if we have a link and a title
            if title and link:
                all_articles.append({"title": title.strip(), "link": link.strip(), "summary": summary.strip()})

    if not all_articles:
        print("  -> [INFO] Scraper: No news articles found for ANY theme in the given date range.")
    else:
        print(f"  -> [SUCCESS] Scraper: Collected {len(all_articles)} articles in total.")

    return all_articles

def get_relevant_image_url(theme):
    """
    Searches for a relevant image using Google Images via SerpApi and returns the first direct image URL that passes basic filters.
    """
    print(f"  -> Scraper: Searching for a relevant image for theme: '{theme}'...")
    if not SERPAPI_API_KEY:
        print("  -> [ERROR] Scraper: SerpApi API key not found, cannot fetch image.")
        return None

    BANNED_IMAGE_SOURCES = ["tiktok.com", "pinterest.com", "facebook.com", "instagram.com"]
    image_query = f"professional real estate {theme} kenya"
    params = {
        "q": image_query,
        "engine": "google_images",
        "ijn": "0",
        "api_key": SERPAPI_API_KEY,
        "tbs": "isz:l,ic:color,itp:photo"
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
    except Exception as e:
        print(f"  -> [ERROR] Scraper: Image search failed. Error: {e}")
        return None

    images = results.get("images_results") or []
    for image_data in images:
        source_domain = (image_data.get('source') or "").lower()
        image_url = image_data.get('original') or image_data.get('thumbnail') or ""
        is_banned = any(b in source_domain for b in BANNED_IMAGE_SOURCES)
        if is_banned:
            continue
        if image_url and image_url.lower().endswith(('.jpg', '.jpeg', '.png')):
            return image_url

    print("  -> [WARNING] Scraper: Could not find a direct suitable image link after checking results.")
    return None