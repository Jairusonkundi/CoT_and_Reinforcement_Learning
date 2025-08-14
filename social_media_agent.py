# social_media_agent.py (Writes to a formatted Markdown .md file - English Version)

import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

def generate_social_posts_to_markdown():
    """
    Reads the final blog post, generates tailored promotional posts for
    Meta and X, and saves them to a clean, formatted Markdown file.
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
    You are a professional social media manager for a real estate company.
    Based on the following blog post, your task is to generate promotional copy for two different platforms: Meta (Facebook/Instagram) and X (Twitter).
    The output must be in a clean, valid JSON format.

    **Instructions:**
    1.  **For the Meta Post:** Write an engaging post (2-3 paragraphs). Start with a hook. Use emojis. Include a clear call-to-action and 5-7 relevant hashtags.
    2.  **For the X (Twitter) Post:** Write a concise, impactful post (under 280 characters). Use a hook. Include a call-to-action and 3-4 highly relevant hashtags.

    **Output MUST be in this strict JSON format:**
    {{
      "meta_post": {{
        "text": "Your generated text for Facebook/Instagram here.",
        "hashtags": "#RealEstateKenya #NairobiHomes #PropertyInvestment ..."
      }},
      "x_post": {{
        "text": "Your generated text for X/Twitter here.",
        "hashtags": "#Kenya #RealEstate #Investing"
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
        
        # --- THIS IS THE CORRECTED SECTION ---
        
        output_filename = "social_media_plan.md"
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            # --- USE ENGLISH HEADERS ---
            f.write("# Social Media Promotion Plan\n\n")
            f.write("This file contains the auto-generated social media posts to promote your blog post.\n\n")
            
            # Write the Meta Post
            meta = social_posts_data.get('meta_post', {})
            f.write("## ✅ Meta (Facebook/Instagram) Post\n\n")
            f.write("```text\n")
            f.write(meta.get('text', 'N/A') + "\n\n")
            f.write(meta.get('hashtags', '') + "\n")
            f.write("```\n\n")
            
            # Write the X Post
            x_post = social_posts_data.get('x_post', {})
            f.write("## ✅ X (Twitter) Post\n\n")
            f.write("```text\n")
            f.write(x_post.get('text', 'N/A') + "\n\n")
            f.write(x_post.get('hashtags', '') + "\n")
            f.write("```\n")

        print(f"--- SUCCESS! ---")
        print(f"Your social media plan has been generated and saved to '{output_filename}'")
        
    except Exception as e:
        print(f"\nAn error occurred during social media post generation: {e}")
        print("--- RAW AI RESPONSE ---")
        print(response_text)

if __name__ == "__main__":
    generate_social_posts_to_markdown()