# main.py
import os
import re
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv

import scraper
import analysis
import generator_agent
import social_media_agent
import feedback   # Feedback scoring + AI evaluation + record_feedback
from feedback_memory import FeedbackMemorySingleton  # Use singleton memory

load_dotenv()

# --- CONFIGURATION ---
INITIAL_SEARCH_THEMES = [
    "Kenya real estate",
    "Nairobi property",
    "Kenya housing market",
    "affordable housing Kenya",
    "Kenya mortgage rates",
    "Kenya commercial real estate",
    "Nairobi rental market",
    "Kenya land prices"
]
SITE_TARGET = None

PROCESSED_BLOG_THEMES_LOG = "processed_blog_themes.log"
CURRENT_SEARCH_THEMES_LOG = "current_search_themes.log"

END_DATE = datetime.today().strftime("%Y-%m-%d")
START_DATE = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")

FEEDBACK_SCORE_THRESHOLD = 0.80  # Stop feedback loop when score ≥ 0.80
MAX_ATTEMPTS = 15  # Increased max attempts for reinforcement

# --- HELPER FUNCTIONS ---
def load_processed_blog_themes():
    if not os.path.exists(PROCESSED_BLOG_THEMES_LOG):
        return set()
    with open(PROCESSED_BLOG_THEMES_LOG, 'r', encoding='utf-8') as f:
        return set(line.strip().lower() for line in f if line.strip())

def save_processed_blog_theme(theme):
    try:
        with open(PROCESSED_BLOG_THEMES_LOG, 'a', encoding='utf-8') as f:
            f.write(theme.lower().strip() + '\n')
    except Exception as e:
        print(f"[ERROR] Main: Could not save processed theme. Error: {e}")

def load_current_search_themes():
    if not os.path.exists(CURRENT_SEARCH_THEMES_LOG):
        return list(INITIAL_SEARCH_THEMES)
    with open(CURRENT_SEARCH_THEMES_LOG, 'r', encoding='utf-8') as f:
        themes = [line.strip() for line in f if line.strip()]
        return themes if themes else list(INITIAL_SEARCH_THEMES)

def save_current_search_themes(themes):
    try:
        with open(CURRENT_SEARCH_THEMES_LOG, 'w', encoding='utf-8') as f:
            for t in themes:
                f.write(t.strip().lower() + '\n')
    except Exception as e:
        print(f"[ERROR] Main: Could not save current search themes. Error: {e}")

def create_markdown_file(title, image_url, blog_post, scores=None):
    clean_title = title.strip().replace('\n', ' ')
    safe_title = re.sub(r'[\\/*?:"<>|]', "", clean_title)[:120]
    filename = f"{safe_title}.md"
    content = f"# {title}\n\n![Blog Post Image]({image_url})\n\n{blog_post}"
    if scores:
        content += "\n\n---\n\n## Feedback Scores\n"
        for k, v in scores.items():
            content += f"- **{k.capitalize()}**: {v}\n"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[SUCCESS] Main: Blog post saved to '{filename}'")
    except Exception as e:
        print(f"[ERROR] Main: Failed to save Markdown file. Error: {e}")

def create_social_markdown_file(title, social_post_text, scores=None):
    clean_title = title.strip().replace('\n', ' ')
    safe_title = re.sub(r'[\\/*?:"<>|]', "", clean_title)[:120]
    filename = f"{safe_title}-social.md"
    content = f"# Social Media Post for: {title}\n\n{social_post_text}"
    if scores:
        content += "\n\n---\n\n## Feedback Scores\n"
        for k, v in scores.items():
            content += f"- **{k.capitalize()}**: {v}\n"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[SUCCESS] Main: Social media post saved to '{filename}'")
    except Exception as e:
        print(f"[ERROR] Main: Failed to save social media Markdown file. Error: {e}")

# --- MAIN WORKFLOW ---
def run_content_engine():
    print("--- LAUNCHING CONTENT CAMPAIGN ENGINE ---")

    if not analysis.configure_ai():
        print("  -> [WARNING] Main: Gemini not configured; feedback will fall back to heuristics.")

    memory = FeedbackMemorySingleton
    current_search_themes = load_current_search_themes()
    processed_blog_themes = load_processed_blog_themes()

    # STEP 0: Expand themes if low
    if not current_search_themes or (len(current_search_themes) < 4 and len(processed_blog_themes) > 3):
        new_search_suggestions = analysis.discover_new_search_themes(current_search_themes, processed_blog_themes)
        if new_search_suggestions:
            updated = list(dict.fromkeys(current_search_themes + new_search_suggestions))
            save_current_search_themes(updated)
            current_search_themes = updated

    # STEP 1: SCRAPE ARTICLES
    all_articles = scraper.get_google_news_articles(
        themes=current_search_themes, start_date=START_DATE, end_date=END_DATE, site_target=SITE_TARGET
    )
    if not all_articles:
        new_search_suggestions = analysis.discover_new_search_themes(current_search_themes, processed_blog_themes)
        if new_search_suggestions:
            all_articles = scraper.get_google_news_articles(
                themes=new_search_suggestions, start_date=START_DATE, end_date=END_DATE, site_target=SITE_TARGET
            )

    if not all_articles:
        print("\n--- ENGINE SHUTDOWN: No articles found. ---")
        return
    print(f"[SUCCESS] Main: Found {len(all_articles)} articles.")

    # STEP 2: ANALYZE THEMES
    all_discussed_themes = analysis.find_highest_discussed_themes(all_articles)
    if not all_discussed_themes:
        print("\n--- ENGINE SHUTDOWN: No themes found. ---")
        return
    print(f"[SUCCESS] Main: Identified {len(all_discussed_themes)} themes.")

    # STEP 3: PICK NEXT THEME
    processed_lower = set(processed_blog_themes)
    next_theme_to_write = None
    for theme in all_discussed_themes:
        if theme.lower() not in processed_lower:
            next_theme_to_write = theme
            break
    if not next_theme_to_write:
        new_search_suggestions = analysis.discover_new_search_themes(current_search_themes, processed_blog_themes)
        if new_search_suggestions:
            updated = list(dict.fromkeys(current_search_themes + new_search_suggestions))
            save_current_search_themes(updated)
            next_theme_to_write = new_search_suggestions[0]
    if not next_theme_to_write:
        print("\n--- ENGINE SHUTDOWN: No new theme available. ---")
        return
    print(f"[SUCCESS] Main: Selected theme: '{next_theme_to_write}'")

    # STEP 4: GENERATE CONTENT
    image_url = scraper.get_relevant_image_url(next_theme_to_write)
    if not image_url:
        image_url = "https://via.placeholder.com/800x400.png?text=Relevant+Image"
    print("[SUCCESS] Main: Found relevant image.")

    # --- Feedback loop for blog ---
    attempt = 1
    accepted_blog = False
    final_blog_scores = None
    final_blog_reasoning = None
    blog_title, blog_post = None, None

    while not accepted_blog:
        blog_title, blog_post = generator_agent.generate_themed_blog_post(next_theme_to_write, all_articles)
        if not blog_post or not blog_title:
            print("[ERROR] Main: Failed to generate blog post.")
            return

        blog_scores, blog_reasoning = feedback.evaluate_blog_ai(blog_title, blog_post)

        if blog_scores.get("overall", 0.0) >= FEEDBACK_SCORE_THRESHOLD:
            accepted_blog = True
            final_blog_scores = blog_scores
            final_blog_reasoning = blog_reasoning
            print(f"[SUCCESS] Blog accepted after {attempt} attempts | Overall score: {blog_scores.get('overall')}")
        attempt += 1

    # Safe memory update (fallback if add_tips not present)
    try:
        memory.add_tips(kind="blog", tips=blog_reasoning)
    except AttributeError:
        try:
            memory.add_feedback("blog", blog_title, next_theme_to_write, final_blog_scores, final_blog_reasoning, attempt-1, accepted=True)
        except Exception:
            pass

    feedback.record_feedback(
        content_type="blog",
        title=blog_title,
        theme=next_theme_to_write,
        scores=final_blog_scores,
        reasoning=final_blog_reasoning,
        attempt=attempt-1,
        accepted=True,
        threshold=FEEDBACK_SCORE_THRESHOLD
    )

    # --- Feedback loop for social post ---
    social_attempt = 1
    accepted_social = False
    final_social_scores = None
    final_social_reasoning = None
    social_post_text = None

    while not accepted_social:
        summary_excerpt = (blog_post or "")[:800]
        social_post_text = social_media_agent.generate_social_post(blog_title, summary_excerpt)
        social_scores, social_reasoning = feedback.evaluate_social_ai(blog_title, social_post_text)

        if social_scores.get("overall", 0.0) >= FEEDBACK_SCORE_THRESHOLD:
            accepted_social = True
            final_social_scores = social_scores
            final_social_reasoning = social_reasoning
            print(f"[SUCCESS] Social post accepted after {social_attempt} attempts | Overall score: {social_scores.get('overall')}")
        social_attempt += 1

    try:
        memory.add_tips(kind="social", tips=social_reasoning)
    except AttributeError:
        try:
            memory.add_feedback("social", blog_title, next_theme_to_write, final_social_scores, final_social_reasoning, social_attempt-1, accepted=True)
        except Exception:
            pass

    feedback.record_feedback(
        content_type="social",
        title=blog_title,
        theme=next_theme_to_write,
        scores=final_social_scores,
        reasoning=final_social_reasoning,
        attempt=social_attempt-1,
        accepted=True,
        threshold=FEEDBACK_SCORE_THRESHOLD
    )

    # STEP 5: SAVE & PUBLISH
    create_markdown_file(blog_title, image_url, blog_post, scores=final_blog_scores)
    create_social_markdown_file(blog_title, social_post_text, scores=final_social_scores)

    final_telegram_message = social_post_text + f"\n\nRead our full analysis: [Link to your blog post about '{blog_title}']"
    try:
        asyncio.run(social_media_agent.post_to_telegram(final_telegram_message))
        print("[SUCCESS] Main: Telegram post published.")
    except Exception:
        pass

    save_processed_blog_theme(next_theme_to_write)
    print("\n--- CONTENT CAMPAIGN ENGINE RUN COMPLETE ---")


if __name__ == "__main__":
    try:
        run_content_engine()
    except Exception as e:
        print(f"[CRITICAL] Main: Unhandled exception. Error: {e}")
