# image_agent.py (Fully Automated Version)

import google.generativeai as genai
import os
from dotenv import load_dotenv
from serpapi import SerpApiClient
import requests # We need this to download the image

def find_and_add_real_image():
    """
    Reads the blog post, uses Gemini to create a search query, uses SerpApi
    to find a real image on Google Images, downloads it, and adds it to the blog.
    """
    print("\n--- Starting Step 4: Fully Automated Image Agent ---")
    
    # Load both API keys from the .env file
    load_dotenv()
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    serpapi_api_key = os.getenv("SERPAPI_API_KEY")

    if not gemini_api_key or not serpapi_api_key:
        print("CRITICAL FAILURE: Gemini or SerpApi API key not found in .env file.")
        return
        
    # Configure the Gemini AI model
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    try:
        with open('blog_draft.md', 'r', encoding='utf-8') as f:
            blog_content = f.read()
    except FileNotFoundError:
        print("CRITICAL FAILURE: blog_draft.md not found. Please run generator.py first.")
        return

    # --- Part A: AI Brain - Generate a Search Query ---
    prompt = f"""
    Based on the following real estate blog post, generate a short, effective search query (3-5 words) for Google Images to find a relevant, high-quality, real photograph. The query should be specific to the content.

    BLOG POST CONTENT:
    ---
    {blog_content}
    ---

    SEARCH QUERY:
    """
    print("Asking AI to generate an effective image search query...")
    
    try:
        response = model.generate_content(prompt)
        image_search_query = response.text.strip()
        print(f"AI generated search query: '{image_search_query}'")
    except Exception as e:
        print(f"An error occurred during search query generation: {e}")
        return

    # --- Part B: AI Eyes - Search for the Image using SerpApi ---
    print(f"Executing image search on Google...")
    try:
        params = {
            "q": image_search_query,
            "engine": "google_images",
            "ijn": "0", # Image search page number
            "gl": "ke", # Geolocation: Kenya
            "api_key": serpapi_api_key
        }
        client = SerpApiClient(params)
        results = client.get_dict()
        
        # Get the URL of the first image result
        if 'images_results' in results and len(results['images_results']) > 0:
            first_image = results['images_results'][0]
            image_url = first_image.get('original')
            print(f"Image found successfully. URL: {image_url}")
        else:
            print("Image search did not return any results.")
            return

    except Exception as e:
        print(f"An error occurred during image search: {e}")
        return

    # --- Part C: AI Hands - Download the Image ---
    if not image_url:
        print("Could not extract a valid image URL from the search results.")
        return
        
    print("Downloading image...")
    try:
        image_response = requests.get(image_url, stream=True, timeout=30)
        image_response.raise_for_status()
        
        # Save the downloaded image
        with open('blog_image.jpg', 'wb') as f:
            for chunk in image_response.iter_content(1024):
                f.write(chunk)
        print("Image downloaded and saved as 'blog_image.jpg'.")
        
    except requests.RequestException as e:
        print(f"Failed to download the image. Error: {e}")
        return

    # Finally, add the image markdown to the top of the blog post file
    image_markdown = f"![Blog Cover Image](blog_image.jpg)\n\n"
    final_blog_content = image_markdown + blog_content

    with open('blog_draft.md', 'w', encoding='utf-8') as f:
        f.write(final_blog_content)

    print("\n--- SUCCESS! ---")
    print("A relevant image was found, downloaded, and added to your blog post.")
    print("The project is now fully and completely automated.")

if __name__ == "__main__":
    find_and_add_real_image()