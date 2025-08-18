# app.py (Final UX Version - Status Log Collapsed by Default)

import streamlit as st
import subprocess
import os
import sys
from PIL import Image
from dotenv import load_dotenv

# --- Load Environment Variables ---
load_dotenv()
TELEGRAM_CHANNEL_USERNAME = os.getenv("TELEGRAM_CHAT_ID", "").replace("@", "")

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Content Bot",
    page_icon="🤖",
    layout="wide"
)

# --- Main App Interface ---
st.title("🤖 AI Content Marketing & Publishing Bot")
st.markdown("Click the button below to launch the fully automated pipeline. It will gather data, write a blog post, find an image, create social media copy, and publish the content directly to Telegram.")

if st.button("🚀 Launch Full Content Pipeline"):

    # --- THIS IS THE KEY CHANGE ---
    # The pipeline log is now collapsed by default. It will only expand if the user clicks on it.
    with st.expander("📊 View Live Pipeline Status Log", expanded=False):
    # --- END OF KEY CHANGE ---
        
        st.write("🧹 Cleaning up old files for a fresh run...")
        files_to_delete = [
            'scraped_articles.csv', 'themes_analysis.json', 'blog_draft.md', 
            'social_media_plan.md', 'social_media_posts.json', 'images/blog_image.jpg'
        ]
        for file in files_to_delete:
            if os.path.exists(file):
                os.remove(file)
        st.write("Cleanup complete.")
        
        st.write("▶️ Starting the main.py pipeline...")
        
        with st.spinner("Pipeline is running... This may take a minute or two."):
            python_executable = os.path.join(sys.prefix, 'Scripts', 'python.exe') if sys.platform == "win32" else os.path.join(sys.prefix, 'bin', 'python')
            process = subprocess.run(
                [python_executable, 'main.py'],
                capture_output=True, text=True, encoding='utf-8', errors='replace'
            )

        st.write("✅ Pipeline finished.")
        
        if process.returncode == 0:
            st.subheader("Full Terminal Log")
            st.code(process.stdout, language='text')
        else:
            st.error("An error occurred during the pipeline execution:")
            st.subheader("Standard Output Log")
            st.code(process.stdout, language='text')
            st.subheader("Error Log")
            st.code(process.stderr, language='text')

    # --- Final Results Display ---
    st.header("🎉 Final Generated Content")
    
    # --- Collapsible Blog Post Section ---
    with st.expander("📖 View Generated Blog Post", expanded=True):
        image_path = "images/blog_image.jpg"
        blog_path = "blog_draft.md"

        if os.path.exists(image_path):
            try:
                image = Image.open(image_path)
                st.image(image, caption='AI-Generated Blog Cover Image', use_column_width=True)
            except Exception as e:
                st.error(f"An error occurred while trying to display the image: {e}")
        else:
            st.warning("Cover image was not generated. Check the log for errors.")

        if os.path.exists(blog_path):
            with open(blog_path, "r", encoding="utf-8") as f:
                full_blog_content = f.read()
                lines = full_blog_content.splitlines()
                text_only_lines = [line for line in lines if not line.strip().startswith('<img')]
                text_only_content = "\n".join(text_only_lines)
                st.markdown(text_only_content)
        else:
            st.warning("Blog post file was not created. Check the log for errors.")

    # --- Collapsible Social Media Plan Section ---
    with st.expander("📱 View Generated Social Media Plan"):
        social_plan_path = "social_media_plan.md"
        if os.path.exists(social_plan_path):
            with open(social_plan_path, "r", encoding="utf-8") as f:
                social_content = f.read()
                st.markdown(social_content)
        else:
            st.warning("Social media plan file was not created. Check the log for errors.")

    # --- Publishing Status Section ---
    st.subheader("🚀 Publishing Status")
    if process.returncode == 0:
        st.success("Content was successfully published to your Telegram Channel!")
        if TELEGRAM_CHANNEL_USERNAME:
            st.markdown(f"**[Click here to view your Telegram channel](https://t.me/{TELEGRAM_CHANNEL_USERNAME})**")
    else:
        st.error("Publishing to Telegram failed. Check the error log in the status section above for details.")