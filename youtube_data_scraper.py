import os
import csv
import googleapiclient.discovery
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled

# YouTube API Setup
API_KEY = "AIzaSyAy4s0VDaiJV9Vzf_iviNzk3XbQ"  # Replace with your actual API key
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def get_youtube_service():
    """
    Build and return the YouTube API client.
    """
    return googleapiclient.discovery.build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY
    )

def fetch_video_data(youtube, genre, max_results=500):
    """
    Fetch video data for a specific genre using the YouTube Data API.
    """
    videos = []
    search_response = youtube.search().list(
        q=genre,
        part="id,snippet",
        type="video",
        maxResults=50,
        order="viewCount"
    ).execute()

    while search_response:
        for item in search_response.get("items", []):
            video_id = item["id"]["videoId"]
            snippet = item["snippet"]
            video_data = {
                "video_id": video_id,
                "title": snippet["title"],
                "description": snippet.get("description", ""),
                "channel_title": snippet["channelTitle"],
                "published_at": snippet["publishedAt"],
            }
            videos.append(video_data)

            # Stop when max_results is reached
            if len(videos) >= max_results:
                break

        if len(videos) >= max_results or "nextPageToken" not in search_response:
            break

        search_response = youtube.search().list(
            q=genre,
            part="id,snippet",
            type="video",
            maxResults=50,
            order="viewCount",
            pageToken=search_response["nextPageToken"]
        ).execute()

    return videos

def fetch_video_details(youtube, video_id):
    """
    Fetch detailed video data, including category, view count, and comment count.
    """
    video_response = youtube.videos().list(
        part="snippet,contentDetails,statistics,recordingDetails,topicDetails",
        id=video_id
    ).execute()

    if video_response["items"]:
        details = video_response["items"][0]
        return {
            "category_id": details["snippet"].get("categoryId", ""),
            "tags": details["snippet"].get("tags", []),
            "duration": details["contentDetails"].get("duration", ""),
            "view_count": details["statistics"].get("viewCount", 0),
            "comment_count": details["statistics"].get("commentCount", 0),
            "location": details.get("recordingDetails", {}).get("location", ""),
            "topics": details.get("topicDetails", {}).get("topicCategories", []),
        }
    return {}

def fetch_captions(video_id):
    """
    Fetch captions for a YouTube video.
    Returns:
    - captions_available (bool): Whether captions are available
    - captions (str): The transcript text or an empty string
    """
    try:
        # Attempt to fetch the transcript in English
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        captions = " ".join([item['text'] for item in transcript])
        return True, captions

    except NoTranscriptFound:
        # Check for other available languages (fallback to auto-generated captions)
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            for transcript in transcript_list:
                if transcript.is_generated:
                    transcript_data = transcript.fetch()
                    captions = " ".join([item['text'] for item in transcript_data])
                    return True, captions
        except Exception:
            return False, ""

    except TranscriptsDisabled:
        return False, ""

    except Exception as e:
        print(f"An error occurred while fetching captions for video {video_id}: {e}")
        return False, ""

def save_to_csv(videos, filename="youtube_videos.csv"):
    """
    Save video data to a CSV file.
    """
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "video_id", "title", "description", "channel_title", "published_at",
            "category_id", "tags", "duration", "view_count", "comment_count",
            "location", "topics", "captions_available", "captions"
        ])
        writer.writeheader()
        writer.writerows(videos)

def main():
    """
    Main function to execute the YouTube data scraping script.
    """
    genre = input("Enter genre: ")
    youtube = get_youtube_service()

    print("Fetching video data...")
    videos = fetch_video_data(youtube, genre)

    print("Fetching video details and captions...")
    for video in videos:
        details = fetch_video_details(youtube, video["video_id"])
        video.update(details)

        captions_available, captions = fetch_captions(video["video_id"])
        video["captions_available"] = captions_available
        video["captions"] = captions

    print(f"Saving data to CSV...")
    save_to_csv(videos)
    print(f"Data saved successfully to 'youtube_videos.csv'.")

if __name__ == "__main__":
    main()
