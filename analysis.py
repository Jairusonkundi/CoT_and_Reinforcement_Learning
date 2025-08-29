# analysis.py

import os
import google.generativeai as genai

# --- CHAIN-OF-THOUGHT PROMPTS ---

THEME_SYNTHESIS_PROMPT = """
You are a senior real estate market analyst. Your task is to identify the single most discussed, commercially significant theme from a collection of recent news article summaries from Kenya.

Let's think step by step:
1.  **Read all summaries:** Carefully review each article title and summary provided below.
2.  **Identify recurring topics:** Look for keywords, concepts, and topics that appear in multiple articles (e.g., "affordable housing," "mortgage rates," "luxury property," "new construction projects").
3.  **Determine the dominant theme:** From the recurring topics, determine which one has the most weight and significance. This is the "highest discussed theme." It's not just about frequency, but also about market impact.
4.  **State the theme clearly:** Conclude with a single, clear sentence stating the dominant theme.

**Respond only with the single sentence identifying the theme.**

**Article Collection:**
---
{articles_text}
---
"""

BLOG_GENERATION_PROMPT = """
You are an expert real estate content creator and market analyst for a Kenyan audience.
Your task is to write a unique, insightful, and comprehensive blog post about a specific, high-level theme, using the provided news articles as sources of information.

**The Highest Discussed Theme is:** "{theme}"

Let's think step by step to create a high-quality, unique article:
1.  **Synthesize a Narrative:** Review the provided articles. Instead of just summarizing one, weave a compelling narrative about the theme. How do these different articles connect to tell a larger story about the Kenyan real estate market?
2.  **Create a Unique Title:** Generate a new, unique, and compelling title for the blog post that captures the essence of the theme. Do not reuse any of the article titles.
3.  **Write an Engaging Introduction:** Start with a strong hook that introduces the theme and explains why it is currently so important for investors and homebuyers in Kenya.
4.  **Develop the Body:** Write at least three body paragraphs. Each paragraph should explore a different facet of the theme, referencing insights from one or more of the provided articles. Do not just copy the summaries; interpret and explain their significance.
5.  **Write a Forward-Looking Conclusion:** Conclude by summarizing the key takeaways and offering a forward-looking perspective or a piece of actionable advice related to the theme.
6.  **Format the Output:** Structure your response as follows, and nothing else:
    
    **Title:** [Your Generated Title]
    **Blog Post:**
    [Your full, multi-paragraph blog post text]

**Source Articles:**
---
{articles_text}
---
"""

# --- AI LOGIC ---

def configure_ai():
    """Configures the Generative AI model with the API key."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("CRITICAL FAILURE: Gemini API key not found in .env file.")
    genai.configure(api_key=api_key)

def find_highest_discussed_theme(articles):
    """Analyzes a list of articles to find the dominant theme."""
    print("Analysis: Analyzing articles to find the highest discussed theme...")
    if not articles:
        return None
        
    articles_text = ""
    for i, article in enumerate(articles, 1):
        articles_text += f"Article {i}:\nTitle: {article['title']}\nSummary: {article['summary']}\n\n"
        
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt = THEME_SYNTHESIS_PROMPT.format(articles_text=articles_text)
        response = model.generate_content(prompt)
        theme = response.text.strip()
        print(f"Analysis: Highest discussed theme identified: '{theme}'")
        return theme
    except Exception as e:
        print(f"Analysis: Error during theme synthesis. Error: {e}")
        return None

def generate_themed_blog_post(theme, articles):
    """Generates a unique blog post and title based on a theme and source articles."""
    print("Analysis: Generating unique blog post based on the theme...")
    if not theme or not articles:
        return None, None
        
    articles_text = ""
    for i, article in enumerate(articles, 1):
        articles_text += f"Article {i}:\nTitle: {article['title']}\nSummary: {article['summary']}\n\n"
        
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt = BLOG_GENERATION_PROMPT.format(theme=theme, articles_text=articles_text)
        response = model.generate_content(prompt)
        
        # Parse the Title and Blog Post from the structured response
        parts = response.text.split("Blog Post:")
        title = parts[0].replace("Title:", "").strip()
        blog_post = parts[1].strip()
        
        print(f"Analysis: Successfully generated blog post with title: '{title}'")
        return title, blog_post
    except Exception as e:
        print(f"Analysis: Error during blog generation. Error: {e}")
        return None, None

def generate_social_media_post(title, blog_post):
    """Generates a unique social media post from the blog content."""
    print("Analysis: Generating unique social media post...")
    if not blog_post:
        return None
        
    social_media_prompt = f"""
    You are a social media manager for a real estate company.
    Based on the blog post below, write a short, unique, and engaging post for Telegram.
    Start with a hook, summarize the key insight, add a call-to-action, and include 3-4 relevant hashtags.

    **Title:** {title}
    **Blog Post:**
    {blog_post}
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(social_media_prompt)
        print("Analysis: Successfully generated social media post.")
        return response.text.strip()
    except Exception as e:
        print(f"Analysis: Error during social media generation. Error: {e}")
        return None