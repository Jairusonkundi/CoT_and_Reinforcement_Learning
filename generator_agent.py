import google.generativeai as genai
import re
import os
from feedback_memory import FeedbackMemorySingleton

BLOG_GENERATION_PROMPT = """
You are an expert real estate content creator and market analyst for a Kenyan audience.
Your task is to write a unique, insightful, and comprehensive blog post about a specific theme using the provided news articles.

The Chosen Theme is: "{theme}"

Tips for improvement from previous runs:
{improvement_tips}

Let's think step by step:
1. Synthesize a Narrative: Weave a compelling narrative about the theme using the provided articles.
2. Create a Unique Title: Generate a new, unique, and compelling title for the blog post.
3. Write the Content: Write an engaging introduction, at least three body paragraphs, and a forward-looking conclusion with actionable advice.
4. Format the Output:

Title: [Your Generated Title]
Blog Post:
[Your full, multi-paragraph blog post text]

Source Articles:
---
{articles_text}
---
"""

def generate_themed_blog_post(theme, articles):
    """
    Generate a blog post for a given theme and list of article dicts.
    articles: List of dicts with 'title' and 'summary' keys.
    Returns: (title, blog_post_text)
    """
    if not theme:
        print("  -> [ERROR] Generator Agent: No theme provided.")
        return None, None

    # Format source articles
    if articles:
        articles_text = "\n".join([f"Title: {a.get('title','')}\nSummary: {a.get('summary','')}\n" for a in articles])
    else:
        articles_text = "No recent articles available. Use general insights about the Kenyan real estate market."

    # ✅ Get improvement tips from memory 
    improvement_tips = FeedbackMemorySingleton.get_improvement_tips(kind="blog")

    try:
        model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        model = genai.GenerativeModel(model_name)
        prompt = BLOG_GENERATION_PROMPT.format(
            theme=theme,
            articles_text=articles_text,
            improvement_tips=improvement_tips
        )
        response = model.generate_content(prompt)
        raw_text = getattr(response, "text", "") or ""
        raw_text = raw_text.strip()

        title_match = re.search(r"(?:\*{0,2}Title\*{0,2}\s*[:\-]\s*)(.+)", raw_text, re.IGNORECASE)
        blog_match = re.search(r"(?:\*{0,2}Blog Post\*{0,2}\s*[:\-]\s*)(.+)", raw_text, re.IGNORECASE | re.DOTALL)

        title = title_match.group(1).strip() if title_match else f"Insights on {theme}"
        blog_post = blog_match.group(1).strip() if blog_match else raw_text

        return title, blog_post

    except Exception as e:
        print(f"  -> [ERROR] Generator Agent: Error during blog generation. Error: {e}")
        return None, None
