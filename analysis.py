# analysis.py (Enhanced with Caching Logic to Save API Quota)

import google.generativeai as genai
import pandas as pd
import os
from dotenv import load_dotenv
import json

def analyze_themes_with_subthemes():
    # --- THIS IS THE NEW CACHING LOGIC ---
    # Before doing anything, check if the output file already exists.
    if os.path.exists('themes_analysis.json'):
        print("\n--- SKIPPING Step 2: AI Theme & Sub-Theme Analysis ---")
        print("Reason: 'themes_analysis.json' already exists. Using cached data to save API quota.")
        # If the file exists, we stop the function here to avoid making a new API call.
        return 
    # --- END OF CACHING LOGIC ---

    print("\n--- Starting Step 2: AI Theme & Sub-Theme Analysis ---")
    
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("CRITICAL FAILURE: Gemini API key not found in .env file.")
        return
        
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('gemini-1.5-flash')

    try:
        df = pd.read_csv('scraped_articles.csv')
    except FileNotFoundError:
        print("CRITICAL FAILURE: scraped_articles.csv not found. Please run scraper.py successfully first.")
        return

    df['id'] = df.index
    df['text_for_analysis'] = df['title'] + ". " + df['summary']
    articles_for_prompt = df[['id', 'text_for_analysis', 'link']].to_dict(orient='records')

    # --- PROMPT ENHANCEMENT: ADDED INSTRUCTIONS FOR SUB-THEMES ---
    prompt = f"""
    Analyze the following list of real estate news article titles and summaries. Your task is to perform a detailed thematic analysis and output the results in a valid JSON format.

    **Instructions:**
    1. Identify the top 5 most prominent main themes.
    2. For each main theme, provide a concise name.
    3. **For each main theme, also identify 2-3 specific sub-themes.**
    4. For each main theme, calculate the percentage of articles that discuss it and provide a number.
    5. For each main theme, list the unique IDs and hyperlinks of the articles that correspond to it.
    
    **Output MUST be in this strict JSON format, including the 'sub_themes' array:**
    {{
      "theme_analysis": [
        {{
          "theme_name": "Name of Theme 1",
          "sub_themes": [
            "Specific sub-theme 1.1",
            "Specific sub-theme 1.2"
          ],
          "percentage_usage": 30,
          "articles": [
            {{"id": 0, "link": "http://link1.com"}}
          ]
        }}
      ]
    }}

    **Article Data:**
    {json.dumps(articles_for_prompt, indent=2)}
    """
    # --- END OF PROMPT ENHANCEMENT ---

    print("Sending data to Gemini AI for detailed analysis. This may take a moment...")
    
    response_text = ""
    try:
        response = model.generate_content(prompt)
        response_text = response.text
        # Clean the response to ensure it's valid JSON
        cleaned_response = response_text.strip().replace("`", "").replace("json", "")
        themes_data = json.loads(cleaned_response)
        
        with open('themes_analysis.json', 'w') as f:
            json.dump(themes_data, f, indent=4)
            
        print("SUCCESS: AI analysis complete. Themes and sub-themes saved to themes_analysis.json")
        
    except Exception as e:
        print(f"An error occurred during AI analysis: {e}")
        print("--- RAW AI RESPONSE ---")
        print(response_text)

if __name__ == "__main__":
    analyze_themes_with_subthemes()