# Fully Autonomous AI News Analyst & Blog Generator

This repository contains a fully automated Python application that gathers recent, hyper-targeted real estate news, uses AI to perform a thematic analysis, uses that analysis to generate a complete blog post, and then automatically finds and inserts a relevant cover image.

The core of this project is a **four-agent pipeline** that demonstrates a professional, robust, and fully autonomous solution for AI-driven content creation.

## Key Features

*   **Hyper-Targeted Data Gathering**:
    *   Utilizes the **SerpApi** to perform a time-filtered (last month) Google search for "real estate" exclusively within a specific news source (`businessdailyafrica.com`).
    *   This approach guarantees 100% relevant, recent data and bypasses all website anti-bot protections.
*   **AI-Powered Thematic Analysis**:
    *   Uses **Google's Gemini 1.5 Flash** model to analyze the content of the gathered articles.
    *   Detects the top 5 most prominent themes in the news and calculates their percentage prevalence.
*   **Data-Driven Blog Generation**:
    *   Orchestrates a second call to the Gemini AI, using the theme analysis as a rich, data-driven prompt to write a complete, well-structured blog post.
*   **Fully Autonomous Image Selection**:
    *   A dedicated AI agent analyzes the final blog text to generate a specific search query.
    *   It then uses SerpApi's Google Images Search to find a relevant photo, downloads it, and automatically inserts it at the top of the final blog post.
*   **Secure & Robust**:
    *   Manages all API keys securely using a `.env` file, which is ignored by Git.

## The AI Pipeline

The application orchestrates four agents in a sequential pipeline:

1.  **`scraper.py` (Data Agent)**:
    *   Connects to SerpApi to execute the targeted site search for articles from the last month.
    *   Saves the raw data into a clean `scraped_articles.csv` file.
2.  **`analysis.py` (Analysis Agent)**:
    *   Reads the raw data and sends it to the Gemini AI for thematic analysis.
    *   Saves a structured JSON response of the top themes to `themes_analysis.json`.
3.  **`generator.py` (Content Agent)**:
    *   Reads the structured JSON analysis and prompts the Gemini AI to write the final blog post text.
    *   Saves the text output to `blog_draft.md`.
4.  **`image_agent.py` (Image Agent)**:
    *   Reads the final blog text.
    *   Uses Gemini to create an intelligent image search query.
    *   Uses SerpApi to find a relevant image on Google Images.
    *   Downloads the image and updates `blog_draft.md` to include it.

## Technologies Used

*   **Python 3**
*   **Google Gemini 1.5 Flash API** (for all NLP, analysis, and content generation)
*   **SerpApi** (for targeted Google Web & Google Images search)
*   **Pandas** (for data handling)
*   **requests** (for API communication and image downloading)
*   **google-search-results** (The official Python library for SerpApi)
*   **Dotenv** (for secure key management)

## Requirements

*   Python 3.10 or higher
*   A **SerpApi API Key** (Free tier available)
*   A **Google Gemini API Key** (Free tier available)

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
3.  **Install dependencies:**
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

Run the four pipeline scripts in order from your terminal to execute the full, hands-free workflow.

1.  **Fetch the data:**
    ```bash
    python scraper.py
    ```
2.  **Analyze the data:**
    ```bash
    python analysis.py
    ```
3.  **Generate the blog post:**
    ```bash
    python generator.py
    ```
4.  **Find and add the cover image:**
    ```bash
    python image_agent.py
    ```
The final, complete output with both text and an image will be available in the **`blog_draft.md`** file.

## Contributing

Contributions are welcome! If you find bugs or have suggestions for improving the application, please feel free to open an issue or submit a pull request.

---
Made with ❤ by [Jairus Onkundi](https://github.com/Jairusonkundi).

[![Linkedin Badge](https://img.shields.io/badge/-JairusOnkundi-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/jairus-onkundi/)](https://www.linkedin.com/in/jairus-onkundi/)
