# analysis.py (Corrected with new model name)
import google.generativeai as genai
import pandas as pd
import os
from dotenv import load_dotenv
import json

def analyze_themes():
    print("\n--- Starting Step 2: AI Theme Analysis ---")
    
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("CRITICAL FAILURE: Gemini API key not found in .env file.")
        return
        
    genai.configure(api_key=api_key)
    
    # --- THIS IS THE FIX: Using the new, correct model name ---
    model = genai.GenerativeModel('gemini-1.5-flash')
    # --- END OF FIX ---

    try:
        df = pd.read_csv('scraped_articles.csv')
    except FileNotFoundError:
        print("CRITICAL FAILURE: scraped_articles.csv not found. Please run scraper.py successfully first.")
        return

    df['id'] = df.index
    df['text_for_analysis'] = df['title'] + ". " + df['summary']
    articles_for_prompt = df[['id', 'text_for_analysis', 'link']].to_dict(orient='records')

    prompt = f"""
    Analyze the following list of real estate news article titles and summaries. Your task is to perform a thematic analysis and output the results in a valid JSON format.
    **Instructions:**
    1. Identify the top 5 most prominent themes.
    2. For each theme, provide a concise name.
    3. For each theme, calculate the percentage of articles that discuss it and provide a number.
    4. For each theme, list the unique IDs and hyperlinks of the articles that correspond to it.
    **Output MUST be in a strict JSON format.**
    **Article Data:**
    {json.dumps(articles_for_prompt, indent=2)}
    """

    print("Sending data to Gemini AI for analysis. This may take a moment...")
    
    response_text = ""
    try:
        response = model.generate_content(prompt)
        response_text = response.text
        cleaned_response = response_text.strip().replace("`", "").replace("json", "")
        themes_data = json.loads(cleaned_response)
        
        with open('themes_analysis.json', 'w') as f:
            json.dump(themes_data, f, indent=4)
            
        print("SUCCESS: AI analysis complete. Themes saved to themes_analysis.json")
        
    except Exception as e:
        print(f"An error occurred during AI analysis: {e}")
        print("--- RAW AI RESPONSE ---")
        print(response_text)

if __name__ == "__main__":
    analyze_themes()