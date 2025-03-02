import logging
from cachetools import TTLCache
from googleapiclient.discovery import build
from configs.settings import YOUTUBE_API_KEY, DEFAULT_REGION, MAX_RESULTS

# Setup logging
logging.basicConfig(filename="logs/idea_generation.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Cache API responses for 10 minutes (600 seconds)
cache = TTLCache(maxsize=10, ttl=600)

def get_youtube_trending_videos(region=DEFAULT_REGION, topic=None, max_results=MAX_RESULTS):
    """Fetch trending video titles from YouTube based on region and topic, with caching."""
    cache_key = f"{region}-{topic}-{max_results}"

    # Check if results are cached
    if cache_key in cache:
        return cache[cache_key]  # Return cached data

    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

        if topic:
            # If a topic is provided, search for trending videos related to the topic
            request = youtube.search().list(
                part="snippet",
                q=topic,  # Search for the specific topic
                type="video",
                regionCode=region,
                maxResults=max_results,
                order="viewCount",
                relevanceLanguage="en",
                safeSearch="moderate"  # Sort by view count to get trending videos
            )
        else:
            # If no topic is given, return general trending videos
            request = youtube.videos().list(
                part="snippet",
                chart="mostPopular",
                regionCode=region,
                maxResults=max_results
            )

        response = request.execute()

        # Extract trending video titles
        trending_videos = [item["snippet"]["title"] for item in response["items"]]

        # Store results in cache
        cache[cache_key] = trending_videos 
        logging.info(f"✅ Successfully fetched {max_results} trending videos for region: {region}, topic: {topic}") 

        return trending_videos

    except Exception as e:
        logging.error(f"❌ YouTube API Error: {str(e)}")  # Log the error
        return [f"❌ Error fetching YouTube trends: {str(e)}"]
