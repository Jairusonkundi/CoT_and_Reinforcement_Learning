# social_media_agent.py (Creates both .md and .json outputs)

import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

def generate_social_media_assets(): # Renamed for clarity
    """
    Reads the blog post, generates social media copy, and saves it in two
    formats: a readable .md file and a structured .json file for other agents.
    """
    print("\n--- Starting Step 5: Social Media Agent ---")
    
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("CRITICAL FAILURE: Gemini API key not found in .env file.")
        return
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    try:
        with open('blog_draft.md', 'r', encoding='utf-8') as f:
            blog_content = f.read()
    except FileNotFoundError:
        print("CRITICAL FAILURE: blog_draft.md not found. Please run generator.py first.")
        return

    prompt = f"""
    You are a professional social media manager... 
    (Your existing, well-crafted prompt for generating JSON is perfect here)
    ...
    **Output MUST be in this strict JSON format:**
    {{
      "meta_post": {{
        "text": "Your generated text for Facebook/Instagram here.",
        "hashtags": "#RealEstateKenya #NairobiHomes ..."
      }},
      "x_post": {{
        "text": "Your generated text for X/Twitter here.",
        "hashtags": "#Kenya #RealEstate ..."
      }}
    }}
    ---
    **BLOG POST CONTENT TO ANALYZE:**
    {blog_content}
    ---
    """

    print("Sending blog content to Gemini AI to generate social media posts...")
    
    response_text = ""
    try:
        response = model.generate_content(prompt)
        response_text = response.text
        
        cleaned_response = response_text.strip().replace("`", "").replace("json", "")
        social_posts_data = json.loads(cleaned_response)
        
        # --- THIS IS THE FIX ---
        
        # 1. Save the structured JSON file for the publisher agent
        with open('social_media_posts.json', 'w', encoding='utf-8') as f:
            json.dump(social_posts_data, f, indent=4)
        print("SUCCESS: Structured social media data saved to 'social_media_posts.json'")

        # 2. Also save the human-readable Markdown file
        md_filename = "social_media_plan.md"
        with open(md_filename, 'w', encoding='utf-8') as f:
            f.write("# Social Media Promotion Plan\n\n")
            f.write("This file contains the auto-generated social media posts to promote your blog post.\n\n")
            
            meta = social_posts_data.get('meta_post', {})
            f.write("## ✅ Meta (Facebook/Instagram) Post\n\n")
            f.write("```text\n")
            f.write(meta.get('text', 'N/A') + "\n\n")
            f.write(meta.get('hashtags', '') + "\n")
            f.write("```\n\n")
            
            x_post = social_posts_data.get('x_post', {})
            f.write("## ✅ X (Twitter) Post\n\n")
            f.write("```text\n")
            f.write(x_post.get('text', 'N/A') + "\n\n")
            f.write(x_post.get('hashtags', '') + "\n")
            f.write("```\n")
        
        print(f"SUCCESS: Human-readable plan saved to '{md_filename}'")
        # --- END OF FIX ---
        
    except Exception as e:
        print(f"\nAn error occurred during social media post generation: {e}")
        print("--- RAW AI RESPONSE ---")
        print(response_text)

if __name__ == "__main__":
    generate_social_media_assets()