# Fully Autonomous AI Content Marketing & Publishing Suite

This repository contains a fully automated Python application that executes a multi-agent pipeline to gather recent real estate news, perform a deep thematic analysis, generate a complete blog post, find a cover image, create social media copy, and **autonomously publish the content to social media.**

The entire pipeline is controlled by a simple, **one-click web interface** built with Streamlit.

## Key Features

*   **One-Click Web Interface**: A user-friendly web app built with **Streamlit** allows anyone to launch the entire content pipeline with a single button click.
*   **Hyper-Targeted Data Gathering**: Utilizes **SerpApi** to perform time-filtered Google searches, guaranteeing relevant, recent data while bypassing anti-bot protections.
*   **AI-Powered Thematic Analysis**: Uses **Google's Gemini 1.5 Flash** to analyze article content, detecting the top 5 themes, their specific sub-themes, and their percentage prevalence.
*   **Data-Driven Blog Generation**: Orchestrates a second call to the Gemini AI, using the rich theme analysis as a prompt to write a complete, well-structured blog post.
*   **Autonomous Image Sourcing**: A dedicated agent uses Gemini and SerpApi to find, download, and optimize a relevant photo, inserting it as a full-width banner.
*   **AI Social Media Management**: A marketing agent analyzes the final blog post and generates ready-to-use promotional copy.
*   **Automated Publishing**: A final agent takes the generated content and **autonomously posts it to a Telegram channel**, completing the end-to-end workflow.
*   **Secure & Robust**: Manages all API keys securely using a `.env` file, which is ignored by Git.

## The AI Pipeline

The application orchestrates six agents in a sequential pipeline, all triggered by a single master script (`main.py`).

1.  **`scraper.py` (Data Agent)**: Connects to SerpApi to execute a targeted search and saves the raw data.
2.  **`analysis.py` (Analysis Agent)**: Reads the data, sends it to Gemini for thematic analysis, and saves a structured JSON response.
3.  **`generator.py` (Content Agent)**: Reads the JSON analysis and prompts Gemini to write the final blog post text.
4.  **`image_agent.py` (Image Agent)**: Finds, downloads, and optimizes a cover image, then updates the blog post to include it.
5.  **`social_media_agent.py` (Marketing Agent)**: Generates promotional social media posts from the final blog content.
6.  **`publisher_agent.py` (Publishing Agent)**: Takes the final content and posts it directly to a Telegram channel.

## Technologies Used

*   **Python 3**
*   **Streamlit** (for the web interface)
*   **Google Gemini 1.5 Flash API** (for all NLP and content generation)
*   **SerpApi** (for targeted Google search)
*   **python-telegram-bot** (for automated publishing)
*   **Pandas** (for data handling)
*   **Pillow** (for image optimization)
*   **requests** (for API communication and image downloading)
*   **Dotenv** (for secure key management)

## Requirements

*   Python 3.10 or higher
*   A **SerpApi API Key**
*   A **Google Gemini API Key**
*   A **Telegram Bot Token** and **Channel Chat ID**

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
        TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN_HERE"
        TELEGRAM_CHAT_ID="@YourTelegramChannelUsername"
        ```

## Usage

The entire application is designed to be run from the Streamlit web interface.

1.  **Launch the Web App:**
    From your activated terminal, run the following command:
    ```bash
    streamlit run app.py
    ```
2.  **Generate & Publish:**
    *   Your web browser will open a new tab with the application.
    *   Click the **"🚀 Launch Full Content Pipeline"** button to execute the entire workflow.
    *   The app will display the status in real-time and show the final generated content and publishing status upon completion.

The final outputs (`blog_draft.md`, `social_media_plan.md`, etc.) will also be saved locally in your project folder.

## Contributing

Contributions are welcome! If you find bugs or have suggestions for improving the application, please feel free to open an issue or submit a pull request.

---
Made with ❤ by [Jairus Onkundi](https://github.com/Jairusonkundi).

