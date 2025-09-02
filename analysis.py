# analysis.py

import google.generativeai as genai
import json
import re
import os

# ----------------- AI CONFIG -----------------
def configure_ai():
    """Configures Google Generative AI with API key."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("  -> [ERROR] Analysis: GEMINI_API_KEY not found in environment.")
        return False
    genai.configure(api_key=api_key)
    return True

# ----------------- PROMPTS -----------------
THEME_EXTRACTION_PROMPT = """
You are an expert analyst of real estate and economic trends in Kenya.

You will be given a set of news articles (titles + summaries).  
Your task is to extract the **main discussed themes** (3–7 themes max).  
Themes should be **short phrases** (2–6 words each).  
Rank them by relevance (most discussed first).  

⚠️ IMPORTANT: Respond ONLY in JSON format as shown:

{
  "themes": [
    "Affordable housing projects in Nairobi",
    "Foreign investment in Kenyan property",
    "Mortgage rate changes",
    "Smart cities and infrastructure",
    "Urbanization challenges"
  ]
}
"""

# ----------------- THEME DISCOVERY -----------------
def find_highest_discussed_themes(articles):
    """Analyzes scraped articles and returns ranked themes."""
    print("  -> Analysis: Analyzing articles to find the highest discussed themes...")

    if not articles:
        print("  -> [WARNING] Analysis: No articles provided.")
        return []

    # Build the text input
    articles_text = "\n".join(
        [f"Title: {a.get('title','')}\nSummary: {a.get('summary','')}" for a in articles]
    )

    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(THEME_EXTRACTION_PROMPT + "\n\n" + articles_text)

        raw_text = response.text.strip()
        # Debug logging
        print("  -> Analysis: Raw AI output (first 300 chars):")
        print(raw_text[:300].replace("\n", " ") + "...")
        
        # First attempt: JSON parsing
        try:
            data = json.loads(raw_text)
            themes = data.get("themes", [])
            if themes:
                return [t.strip() for t in themes]
        except json.JSONDecodeError:
            pass

        # Fallback: extract JSON substring if Gemini wrapped it in markdown
        json_match = re.search(r"\{[\s\S]*\}", raw_text)
        if json_match:
            try:
                data = json.loads(json_match.group(0))
                themes = data.get("themes", [])
                if themes:
                    return [t.strip() for t in themes]
            except:
                pass

        # Last fallback: extract lines starting with "-"
        themes = re.findall(r"-\s*(.+)", raw_text)
        if themes:
            return [t.strip() for t in themes]

        print("  -> [WARNING] Analysis: AI returned no parsable themes.")
        return []

    except Exception as e:
        print(f"  -> [ERROR] Analysis: Failed during theme extraction. Error: {e}")
        return []

# ----------------- SEARCH THEME DISCOVERY -----------------
DISCOVER_NEW_SEARCH_PROMPT = """
You are helping expand search coverage for Kenyan real estate content.

Given the current themes and past covered themes, suggest 3–5 NEW,  
more specific Google News search queries. These should be narrower than "Kenya real estate" —  
focus on current events, policy, or investment.

Respond ONLY in JSON:

{
  "search_queries": [
    "Nairobi affordable housing projects 2025",
    "Kenya mortgage rates and banking policy",
    "Smart city infrastructure Nairobi",
    "Foreign investment in Kenyan real estate"
  ]
}
"""

def discover_new_search_themes(current_themes, processed_themes):
    """Suggests new search themes to broaden coverage."""
    print("  -> Analysis: Discovering new search themes...")
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        prompt = DISCOVER_NEW_SEARCH_PROMPT + f"""

Current search themes: {list(current_themes)}
Already covered themes: {list(processed_themes)}
"""
        response = model.generate_content(prompt)
        raw_text = response.text.strip()

        # Debug logging
        print("  -> Analysis: Raw AI discovery output (first 200 chars):")
        print(raw_text[:200].replace("\n", " ") + "...")

        # Parse JSON
        try:
            data = json.loads(raw_text)
            return [q.strip() for q in data.get("search_queries", [])]
        except:
            # Fallback: regex list extraction
            queries = re.findall(r"-\s*(.+)", raw_text)
            return [q.strip() for q in queries] if queries else []

    except Exception as e:
        print(f"  -> [ERROR] Analysis: Failed to discover new search themes. Error: {e}")
        return []