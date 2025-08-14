# Fully Autonomous AI News Analyst & Content Marketing Suite

This repository contains a fully automated Python application that executes a multi-agent pipeline to gather recent real estate news, perform a deep thematic analysis, generate a complete blog post, find a relevant cover image, and finally, create social media copy to promote the article.

This project demonstrates a professional, robust, and fully autonomous solution for AI-driven content creation and marketing.

## Key Features

*   **Hyper-Targeted Data Gathering**: Utilizes **SerpApi** to perform time-filtered Google searches, guaranteeing relevant, recent data while bypassing common anti-bot protections.
*   **AI-Powered Thematic Analysis**: Uses **Google's Gemini 1.5 Flash** to analyze article content, detecting the top 5 themes, their specific sub-themes, and their percentage prevalence.
*   **Data-Driven Blog Generation**: Orchestrates a second call to the Gemini AI, using the rich theme analysis as a prompt to write a complete, well-structured blog post.
*   **Autonomous Image Sourcing**: A dedicated agent uses Gemini to create an intelligent image search query based on the blog's content, finds a real photo via SerpApi, downloads it, and inserts it as a full-width banner.
*   **AI Social Media Management**: A final agent analyzes the blog post and generates ready-to-use promotional copy for Meta (Facebook/Instagram) and X (Twitter).
*   **Secure & Robust**: Manages all API keys securely using a `.env` file, which is ignored by Git.

## The AI Pipeline

The application orchestrates five agents in a sequential pipeline. Each script must be run in order to pass the correct data to the next agent.

1.  **`scraper.py` (Data Agent)**: Connects to SerpApi to execute a targeted site search and saves the raw data to `scraped_articles.csv`.
2.  **`analysis.py` (Analysis Agent)**: Reads the data, sends it to Gemini for thematic and sub-theme analysis, and saves a structured JSON response to `themes_analysis.json`.
3.  **`generator.py` (Content Agent)**: Reads the JSON analysis and prompts Gemini to write the final blog post text to `blog_draft.md`.
4.  **`image_agent.py` (Image Agent)**: Reads the blog text, uses Gemini and SerpApi to find and download a relevant cover image, and updates `blog_draft.md` to include it.
5.  **`social_media_agent.py` (Marketing Agent)**: Reads the final blog post and prompts Gemini to create promotional social media posts, saving them to `social_media_plan.md`.

## Technologies Used

*   **Python 3**
*   **Google Gemini 1.5 Flash API** (for all NLP, analysis, and content generation)
*   **SerpApi** (for targeted Google Web & Google Images search)
*   **Pandas** (for data handling)
*   **requests** (for API communication and image downloading)
*   **Dotenv** (for secure key management)

## Requirements

*   Python 3.10 or higher
*   A **SerpApi API Key**
*   A **Google Gemini API Key**

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Jairusonkundi/ai_blog-generator.git
    cd ai_blog-generator
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    # Create the venv
    python -m venv venv
    # Activate on Windows
    venv\Scripts\activate
    # Activate on macOS/Linux
    source venv/bin/activate
    ```
3.  **Install dependencies from `requirements.txt`:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure your API keys:**
    *   Create a file in the root of the project named `.env`
    *   Add your keys to this file like so:
        ```
        SERPAPI_API_KEY="YOUR_SERPAPI_KEY_HERE"
        GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
        ```

## Usage

Run the five pipeline scripts **in order** from your terminal to execute the full, hands-free workflow. Each script's success is required for the next to work.

1.  **Fetch the data:**
    ```bash
    python scraper.py
    ```
2.  **Analyze the data:**
    ```bash
    python analysis.py
    ```
3.  **Generate the blog post text:**
    ```bash
    python generator.py
    ```
4.  **Find and add the cover image:**
    ```bash
    python image_agent.py
    ```
5.  **Generate the social media posts:**
    ```bash
    python social_media_agent.py
    ```

The final outputs will be:
*   **`blog_draft.md`**: The complete blog post with its cover image.
*   **`social_media_plan.md`**: The ready-to-use social media copy.

## Contributing

Contributions are welcome! If you find bugs or have suggestions for improving the application, please feel free to open an issue or submit a pull request.


Made with ❤ by [Jairus Onkundi](https://github.com/Jairusonkundi).
