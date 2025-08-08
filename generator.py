# generator.py (Final Version - Corrected with Real JSON Keys)
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

def generate_blog_post_final():
    """
    Loads the theme analysis and generates a blog post using the correct
    JSON keys provided by the AI. This is the final working version.
    """
    print("\n--- Starting Step 3: AI Blog Post Generation ---")

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("CRITICAL FAILURE: Gemini API key not found in .env file.")
        return
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    try:
        with open('themes_analysis.json', 'r') as f:
            analysis_data = json.load(f)
    except FileNotFoundError:
        print("CRITICAL FAILURE: themes_analysis.json not found. Please run analysis.py first.")
        return

    # --- THIS IS THE FINAL FIX ---
    # We now look for the correct main key: "themes"
    if 'themes' in analysis_data and isinstance(analysis_data['themes'], list):
        list_of_themes = analysis_data['themes']
    else:
        print("CRITICAL FAILURE: The JSON from analysis.py does not contain a 'themes' list.")
        return
    # --- END OF FIX ---

    themes_for_prompt = ""
    for theme in list_of_themes:
        # --- AND WE USE THE CORRECT SUB-KEYS: "name" and "percentage" ---
        if isinstance(theme, dict) and 'name' in theme and 'percentage' in theme:
            themes_for_prompt += f"- **Theme:** {theme.get('name')} ({theme.get('percentage')}% of news coverage)\n"

    if not themes_for_prompt:
        print("Could not extract any valid themes from themes_analysis.json. Cannot generate blog post.")
        return

    prompt = f"""
    Act as an expert real estate analyst and blogger. Your target audience is potential property buyers and investors.
    Write a captivating and informative blog post titled: **"Data-Driven Insights: The Top Trends in Real Estate Today."**
    **Instructions:**
    1. Start with a strong introduction.
    2. Use the themes and their percentage usage provided below as the foundation for the blog post.
    3. For each theme, create a compelling heading and explicitly mention its percentage of news coverage.
    4. Conclude with a forward-looking summary and a strong call to action.
    **Data-Driven Themes to Use:**
    {themes_for_prompt}
    """

    print("Sending themes to Gemini AI to generate the blog post...")
    
    try:
        response = model.generate_content(prompt)
        
        with open('blog_draft.md', 'w', encoding='utf-8') as f:
            f.write(response.text)

        print("--- SUCCESS! ---")
        print("Your final blog post has been generated and saved to blog_draft.md")
        print("The entire project is now complete.")

    except Exception as e:
        print(f"An error occurred during blog post generation: {e}")

if __name__ == "__main__":
    generate_blog_post_final()