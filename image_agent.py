# image_agent.py (Updated to accept content as an argument)

import google.generativeai as genai
import os
from dotenv import load_dotenv
from serpapi import SerpApiClient
import requests

# --- THE FUNCTION DEFINITION HAS CHANGED ---
def find_and_add_real_image(blog_content):
    """
    Takes blog content as an input, finds a real image, downloads it,
    and rewrites the final blog_draft.md with the image prepended.
    """
    print("\n--- Starting Step 4: Fully Automated Image Agent ---")
    
    # --- THIS CHECK IS NOW AT THE START ---
    if not blog_content:
        print("CRITICAL FAILURE: No blog content was provided to the Image Agent.")
        return

    load_dotenv()
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    serpapi_api_key = os.getenv("SERPAPI_API_KEY")

    if not gemini_api_key or not serpapi_api_key:
        print("CRITICAL FAILURE: Gemini or SerpApi API key not found in .env file.")
        return
        
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # --- WE NO LONGER READ THE FILE HERE ---

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
            "q": image_search_query, "engine": "google_images", "ijn": "0",
            "gl": "ke", "api_key": serpapi_api_key
        }
        client = SerpApiClient(params)
        results = client.get_dict()
        
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
        
        os.makedirs("images", exist_ok=True)
        image_save_path = os.path.join("images", "blog_image.jpg")
        
        with open(image_save_path, 'wb') as f:
            for chunk in image_response.iter_content(1024):
                f.write(chunk)
        print(f"Image downloaded and saved to '{image_save_path}'.")
        
    except requests.RequestException as e:
        print(f"Failed to download the image. Error: {e}")
        return

    # --- Prepend the image to the content and rewrite the final file ---
    image_html = f'<img src="images/blog_image.jpg" alt="Blog Cover Image" style="width: 100%;">\n\n'
    final_blog_content = image_html + blog_content
    
    with open('blog_draft.md', 'w', encoding='utf-8') as f:
        f.write(final_blog_content)

    print("\n--- SUCCESS! ---")
    print("A relevant image was found, downloaded, and added to your blog post.")

if __name__ == "__main__":
    # This part is now mainly for testing the agent in isolation.
    # It requires a blog_draft.md to exist to run this way.
    try:
        with open('blog_draft.md', 'r', encoding='utf-8') as f:
            test_content = f.read()
        find_and_add_real_image(test_content)
    except FileNotFoundError:
        print("To test image_agent.py directly, a 'blog_draft.md' file must exist.")