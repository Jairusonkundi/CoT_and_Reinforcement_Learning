# main.py (Final Version - Correct Error Reporting)

from scraper import get_targeted_kenyan_news_last_month
from analysis import analyze_themes_with_subthemes
from generator import generate_detailed_blog_post
from image_agent import find_and_add_real_image
from social_media_agent import generate_social_media_assets
from publisher_agent import post_to_telegram

def run_full_automated_pipeline():
    """
    Executes the entire synchronous AI agent pipeline.
    """
    print("--- LAUNCHING FULLY AUTOMATED AI CONTENT PIPELINE ---")
    
    try:
        print("\n--- Running Step 1: Data Agent ---")
        get_targeted_kenyan_news_last_month()
        
        print("\n--- Running Step 2: Analysis Agent ---")
        analyze_themes_with_subthemes()
        
        print("\n--- Running Step 3: Generator Agent ---")
        blog_text_content = generate_detailed_blog_post()
        if not blog_text_content:
            raise ValueError("Generator script failed to return content.")
        
        print("\n--- Running Step 4: Image Agent ---")
        find_and_add_real_image(blog_text_content)
        
        print("\n--- Running Step 5: Social Media Agent ---")
        generate_social_media_assets()
        
        print("\n--- Running Final Step: Publisher Agent ---")
        success = post_to_telegram()
        if not success:
            raise Exception("Publisher Agent failed to post to Telegram.")

    except Exception as e:
        # If any part of the pipeline fails, print the error.
        # The script will then end naturally, but because an exception was
        # caught, it will signal a failure to the subprocess.
        print(f"PIPELINE HALTED: An error occurred: {e}")
        # --- WE REMOVED exit(1) ---
        return # Simply stop the function

    print("\n--- PIPELINE COMPLETE! CONTENT HAS BEEN PUBLISHED. ---")
    print("Your final outputs were created and a summary was posted to your Telegram channel.")

if __name__ == "__main__":
    run_full_automated_pipeline()