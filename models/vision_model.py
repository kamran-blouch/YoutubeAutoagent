import requests
from configs.settings import PEXELS_API

PEXELS_URL = "https://api.pexels.com/videos/search"

def search_videos_on_pexels(query, num_results=7):
    """
    Searches for multiple videos on Pexels based on the selected topic.
    """
    headers = {"Authorization": PEXELS_API}
    params = {"query": query, "per_page": num_results}
    response = requests.get(PEXELS_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        videos = response.json().get("videos", [])
        return [video["video_files"][0]["link"] for video in videos if video.get("video_files")]
    else:
        print(f"❌ Pexels API Error: {response.status_code}")
        return []
