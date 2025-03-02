import re
import json
from models.youtube_scraper import get_youtube_trending_videos
from configs.settings import DEFAULT_REGION, MAX_RESULTS


def clean_video_title(title):
    """Remove hashtags, special characters, and extra spaces from video titles."""
    title = re.sub(r"[#@].*?", "", title)  # Remove hashtags and @mentions
    title = re.sub(r"[^a-zA-Z0-9\s]", "", title)  # Keep only letters, numbers, and spaces
    title = title.strip()  # Remove leading/trailing spaces
    return title.title()  # Capitalize first letter of each word


def get_trending_ideas(region=DEFAULT_REGION, topic=None, max_results=MAX_RESULTS, return_json=True):
    trending_videos = get_youtube_trending_videos(region, topic, max_results)
    cleaned_trending_videos = [clean_video_title(video) for video in trending_videos if len(video) > 5]

    result = {
        "region": region,
        "topic": topic if topic else "General Trends",
        "trending_topics": cleaned_trending_videos
    }

    return json.dumps(result, indent=2) if return_json else result  # ✅ Handles both cases




if __name__ == "__main__":
    print(get_trending_ideas("US", "Artificial Intelligence", 5))  # Example: Get AI trending topics in the US
