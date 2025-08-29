# main.py

import os
import random
from dotenv import load_dotenv
import telegram
import asyncio

# Import our custom modules
import scraper
import analysis

# --- CORE CONFIGURATION FOR THIS RUN ---
# Keywords & Tags: The specific real estate themes to search for.
SEARCH_THEMES = ["real estate"]

# The specific website we trust for high-quality news.
SITE_TARGET = "businessdailyafrica.com"

# The PRECISE timeframe for this run.
START_DATE = "2025-07-01"
END_DATE = "2025-07-31"

# The specific number of articles to scrape, chosen randomly each time.
# Let's use a range, e.g., between 8 and 15 articles.
NUM_ARTICLES_TO_SCRAPE = random.randint(8, 15)
# --- END OF CONFIGURATION ---


def create_markdown_file(title, image_url, blog_post):
    """Creates a well-formatted Markdown file for the blog post."""
    print("Orchestrator: Creating Markdown file...")
    
    # Sanitize the title to create a safe filename
    safe_filename = "".join(x for x in title if x.isalnum() or x in " ").strip() + ".md"
    
    # This structure is standard and looks great in viewers like VS Code.
    content = f"""# {title}

![Blog Post Image]({image_url})

{blog_post}
"""
    
    try:
        with open(safe_filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Orchestrator: Successfully saved blog post to '{safe_filename}'")
    except Exception as e:
        print(f"Orchestrator: Failed to save Markdown file. Error: {e}")

async def post_to_telegram(message):
    """Sends a message to the configured Telegram channel."""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not bot_token or not chat_id:
        print("Orchestrator: Telegram credentials not found. Skipping post.")
        return
    try:
        bot = telegram.Bot(token=bot_token)
        await bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
        print("Orchestrator: Successfully posted to Telegram.")
    except Exception as e:
        print(f"Orchestrator: Failed to post to Telegram. Error: {e}")

def run_content_engine():
    """Executes the full, intelligent content generation workflow."""
    print("--- LAUNCHING INTELLIGENT CONTENT ENGINE V2 ---")
    
    # STEP 1: SCRAPE NEWS ARTICLES
    print(f"\n[STEP 1/6] Scraping {NUM_ARTICLES_TO_SCRAPE} news articles...")
    articles = scraper.get_google_news_articles(
        themes=SEARCH_THEMES, start_date=START_DATE, end_date=END_DATE,
        site_target=SITE_TARGET, num_articles=NUM_ARTICLES_TO_SCRAPE
    )
    if not articles:
        print("Engine shutting down: No articles were scraped.")
        return
        
    # STEP 2: IDENTIFY HIGHEST DISCUSSED THEME
    print("\n[STEP 2/6] Analyzing articles to synthesize the dominant theme...")
    highest_discussed_theme = analysis.find_highest_discussed_theme(articles)
    if not highest_discussed_theme:
        print("Engine shutting down: Could not determine the theme.")
        return
        
    # STEP 3: SCRAPE FOR A RELEVANT IMAGE
    print("\n[STEP 3/6] Searching for a relevant blog post image...")
    image_url = scraper.get_relevant_image_url(highest_discussed_theme)
    if not image_url:
        print("Warning: Could not find a valid image. Using a placeholder.")
        image_url = "https://via.placeholder.com/800x400.png?text=Relevant+Image" # A fallback image
        
    # STEP 4: GENERATE UNIQUE BLOG POST & TITLE
    print("\n[STEP 4/6] Generating unique blog post and title about the theme...")
    blog_title, blog_post = analysis.generate_themed_blog_post(highest_discussed_theme, articles)
    if not blog_post:
        print("Engine shutting down: Failed to generate blog post.")
        return
    
    # STEP 5: CREATE THE MARKDOWN FILE
    print("\n[STEP 5/6] Creating final Markdown blog post file...")
    create_markdown_file(blog_title, image_url, blog_post)
    
    # STEP 6: GENERATE & POST TO SOCIAL MEDIA
    print("\n[STEP 6/6] Generating social media post and publishing...")
    social_post_text = analysis.generate_social_media_post(blog_title, blog_post)
    if not social_post_text:
        print("Warning: Failed to generate social media post. Skipping Telegram post.")
    else:
        final_telegram_message = social_post_text + f"\n\nRead our full analysis on the blog: [Link to '{blog_title}']"
        asyncio.run(post_to_telegram(final_telegram_message))
    
    print("\n--- INTELLIGENT CONTENT ENGINE RUN COMPLETE ---")

if __name__ == "__main__":
    load_dotenv()
    analysis.configure_ai()
    run_content_engine()