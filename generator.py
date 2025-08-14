# generator.py (Upgraded to use Themes and Sub-Themes)
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

def generate_detailed_blog_post():
    """
    Loads the detailed theme and sub-theme analysis and generates a comprehensive
    blog post using this richer data.
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

    # --- THIS IS THE UPDATE: We check for the 'theme_analysis' key ---
    if 'theme_analysis' not in analysis_data or not isinstance(analysis_data['theme_analysis'], list):
        print("CRITICAL FAILURE: The JSON from analysis.py does not contain a 'theme_analysis' list.")
        print("Please ensure your analysis.py script is creating the correct JSON structure.")
        return
    # --- END OF UPDATE ---

    list_of_themes = analysis_data['theme_analysis']
    
    # --- PROMPT DATA PREPARATION: We now format both themes and sub-themes ---
    themes_for_prompt = ""
    for theme in list_of_themes:
        # Check if the dictionary has the keys we expect
        if all(k in theme for k in ['theme_name', 'percentage_usage', 'sub_themes']):
            # Main theme line
            themes_for_prompt += f"- **Theme:** {theme['theme_name']} ({theme['percentage_usage']}% of news coverage)\n"
            
            # Sub-themes list
            if theme['sub_themes']:
                themes_for_prompt += "  - **Key Sub-Themes:**\n"
                for sub_theme in theme['sub_themes']:
                    themes_for_prompt += f"    - {sub_theme}\n"
        themes_for_prompt += "\n" # Add a space between themes for clarity
    # --- END OF PROMPT DATA PREPARATION ---

    if not themes_for_prompt:
        print("Could not extract any valid themes from themes_analysis.json. Cannot generate blog post.")
        return

    # --- FINAL PROMPT: Now instructs the AI to use the sub-themes ---
    prompt = f"""
    Act as an expert real estate analyst and blogger. Your target audience is potential property buyers and investors in Kenya.
    Write a captivating and highly detailed blog post titled: **"Deep Dive: The Top 5 Trends Shaping Kenya's Real Estate Market."**
    
    **Instructions:**
    1. Start with a strong, engaging introduction that hooks the reader.
    2. Use the themes, their percentage usage, and their specific sub-themes provided below as the foundation for the blog post.
    3. For each main theme, create a compelling heading. In the body of each section, first discuss the main theme, and then **use the provided sub-themes to add specific details, examples, and depth.**
    4. Mention the percentage of news coverage for each main theme to show it's a data-driven analysis.
    5. Conclude with a forward-looking summary and a strong call to action for readers to get in touch.

    **Data-Driven Themes and Sub-Themes to Use:**
    {themes_for_prompt}
    """
    # --- END OF FINAL PROMPT ---

    print("Sending detailed themes to Gemini AI to generate the final blog post...")
    
    try:
        response = model.generate_content(prompt)
        
        with open('blog_draft.md', 'w', encoding='utf-8') as f:
            f.write(response.text)

        print("--- SUCCESS! ---")
        print("Your detailed blog post has been generated and saved to blog_draft.md")
      

    except Exception as e:
        print(f"An error occurred during blog post generation: {e}")

if __name__ == "__main__":
    generate_detailed_blog_post()