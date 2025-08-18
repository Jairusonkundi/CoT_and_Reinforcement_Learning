# publisher_agent.py (Final Version - Link Removed)

import os
import json
from dotenv import load_dotenv
import telegram
import asyncio

# This is the original async function
async def _send_telegram_message(bot_token, chat_id, message, image_path):
    bot = telegram.Bot(token=bot_token)
    with open(image_path, 'rb') as photo:
        await bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=message,
            parse_mode='Markdown'
        )

# This is the synchronous wrapper function
def post_to_telegram():
    """
    A synchronous wrapper that prepares the content and then runs the
    asynchronous sending function. This is compatible with any script.
    """
    print("\n--- Starting Final Step: Publishing Agent for Telegram ---")
    
    load_dotenv()
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("CRITICAL FAILURE: Telegram credentials not found in .env file.")
        return False

    try:
        with open('themes_analysis.json', 'r', encoding='utf-8') as f:
            analysis = json.load(f)
        with open('social_media_posts.json', 'r', encoding='utf-8') as f:
            social_posts = json.load(f)
    except FileNotFoundError:
        print("CRITICAL FAILURE: Required JSON files not found.")
        return False

    try:
        blog_title = "Deep Dive: The Top 5 Trends Shaping Kenya's Real Estate Market"
        first_theme = analysis['theme_analysis'][0]['theme_name']
        meta_post_text = social_posts['meta_post']['text']
        image_path = "images/blog_image.jpg"
        
        # --- THIS IS THE FINAL CHANGE ---
        # The link has been removed from the end of the message.
        final_message = f"*{blog_title}*\n\nA quick look at today's top trend: *{first_theme}*.\n\n{meta_post_text}"
        # --- END OF FINAL CHANGE ---

    except (KeyError, IndexError):
        print("Could not format the message. Check JSON file structure.")
        return False

    try:
        print("Connecting to Telegram and sending the post...")
        asyncio.run(_send_telegram_message(bot_token, chat_id, final_message, image_path))
        
        print("--- ✅ SUCCESS! ---")
        print("Message and image have been posted to your Telegram channel.")
        return True

    except FileNotFoundError:
        print(f"CRITICAL FAILURE: Image not found at '{image_path}'.")
        return False
    except Exception as e:
        print(f"An error occurred while posting to Telegram: {e}")
        return False

if __name__ == "__main__":
    post_to_telegram()