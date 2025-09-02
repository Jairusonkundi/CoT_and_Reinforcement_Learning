# social_media_agent.py

import os
import json
import aiohttp
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Load keys
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# ----------------- SOCIAL POST GENERATION -----------------
SOCIAL_PROMPT_TEMPLATE = """
You are an expert social media copywriter for a real estate insights brand in Kenya, known for crafting concise, engaging, and highly clickable Telegram content.

Your task is to transform the provided blog title and summary into a compelling, short Telegram post that captures attention and drives clicks.

Blog Title: {title}

Blog Summary: {summary}
# The actual blog link will be appended by the system after generation.


**Strict Guidelines for a Top-Notch Post:**

1.  **Post Structure & Title:** The output *must* begin with the exact  {title} provided, serving as the title for the Telegram post. This title should be followed by a single line break.

2.  **Purpose & Relevance:** The main content of the post must instantly convey the core value or a key, actionable insight from the blog, ensuring it is highly relevant and enticing to a Kenyan real estate audience. Extract the most critical takeaway or benefit.

3.  **Conciseness & Optimal Length (Main Content):** The main content (excluding the title) should be exactly 2 to 4 sentences. Each sentence should be impactful, easy to digest quickly, and avoid unnecessary words.

4.  **Clarity & Readability:** Use simple, direct language. The entire post must be crystal clear, immediately understandable, and free of jargon that would hinder quick comprehension.

5.  **Engagement & Visual Hook (Emojis):** Integrate 1-2 highly relevant and visually appealing emojis (e.g., 🏠, 📈, 💡, 💰, 📊) at the beginning of the main content or strategically within the text to grab attention and boost engagement without clutter.

6.  **Tone & Persona:** Maintain a professional yet friendly and approachable tone, reflecting an expert who is also helpful and engaging.

7.  **Clear Call-to-Action (CTA):** End the main content with a direct, compelling call-to-action phrase (e.g., "Dive into the full analysis here", "Unlock these insights now"). **Do NOT include the link itself in the output.** Your system will append the actual link after this phrase.


Respond ONLY with the final, polished Telegram post text, including the generated title and the line break as specified. Do not include any introductory or concluding remarks, just the post itself.
"""

def generate_social_post(title: str, summary: str) -> str:
    """Generates a social media post from blog title + summary using Gemini."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        prompt = SOCIAL_PROMPT_TEMPLATE.format(title=title, summary=summary)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[ERROR] SocialMediaAgent: Failed to generate social post. Error: {e}")
        return f"{title} — {summary}"

# ----------------- TELEGRAM PUBLISH -----------------
async def _send_telegram_message_async(message: str):
    """Internal async sender for Telegram."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[ERROR] SocialMediaAgent: Telegram credentials not set.")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload) as resp:
                if resp.status == 200:
                    print("[SUCCESS] SocialMediaAgent: Post sent to Telegram.")
                    return True
                else:
                    print(f"[ERROR] SocialMediaAgent: Telegram API failed with status {resp.status}")
                    return False
    except Exception as e:
        print(f"[ERROR] SocialMediaAgent: Telegram send failed. Error: {e}")
        return False

def post_to_telegram(message: str):
    """Public function to send a Telegram message synchronously."""
    try:
        asyncio.run(_send_telegram_message_async(message))
    except RuntimeError:
        # If already inside an event loop (rare), fallback
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_send_telegram_message_async(message))
