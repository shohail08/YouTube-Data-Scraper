

# YouTube Data Scraper

A Python script to scrape video data (e.g., video title, description, view count) and captions from YouTube videos for a given genre using the YouTube Data API v3.

## Features

- Scrapes top 500 videos for a specific genre from YouTube.
- Collects data such as:
  - Video URL
  - Title
  - Description
  - Channel Title
  - Keywords
  - Published Date
  - Video Duration
  - View Count
  - Comment Count
  - Captions (if available)
- Saves all the collected data to a CSV file.
  
## Prerequisites

Before you can run the scraper, you need a valid **YouTube Data API v3** key. 

1. **Generate Your Own YouTube API Key:**
   - Please follow the instructions [here](https://developers.google.com/youtube/v3/getting-started) to create a YouTube API key.
   - After creating your key, you will need to replace the placeholder in the script with your **own API key**.

2. **Important Note**: The API key in this project is **restricted** to my personal use, so you must provide your own API key in order to use the script.

## Setup

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/YouTube-Data-Scraper.git
   cd YouTube-Data-Scraper
   ```

2. **Create a virtual environment** (optional, but recommended):

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:

   - For **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```

   - For **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## How to Use

1. Open the `youtube_data_scraper.py` file.
2. Replace the placeholder `YOUR_YOUTUBE_API_KEY` with your own YouTube API key.
   ```python
   youtube = build('youtube', 'v3', developerKey='YOUR_YOUTUBE_API_KEY')
   ```
3. Run the script:

   ```bash
   python youtube_data_scraper.py
   ```

4. When prompted, enter the genre you want to scrape (e.g., `Technology`).

5. The data will be saved in a CSV file called `youtube_video_data.csv` in the project directory.

## Important Notes

- **API Quota**: Keep in mind that the YouTube Data API has daily quotas. If you exceed this, you may need to wait or request an increase from Google.
- If you encounter any issues with the API or need assistance, please check the [YouTube Data API documentation](https://developers.google.com/youtube/v3).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### **How to Add Your Own API Key**:
In the script, there’s a line where the API key is required:

```python
youtube = build('youtube', 'v3', developerKey='YOUR_YOUTUBE_API_KEY')
```

Make sure to replace `'YOUR_YOUTUBE_API_KEY'` with the API key you generated on the [Google Developers Console](https://console.developers.google.com/).

Let me know if you need any adjustments or more details added!