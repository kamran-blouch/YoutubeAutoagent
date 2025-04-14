import requests
import time
from configs.settings import GROQ_API_KEY

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def optimize_seo(video_title: str, max_retries: int = 5) -> dict | None:
    """
    Generates an SEO-optimized title, description, tags, and hashtags for the given video title.
    Includes hashtags in title and description. Retries on API overload.
    """
    prompt = f"""
    Optimize the SEO for the following YouTube video title:
    
    Title: "{video_title}"
    
    Provide:
    1. A more SEO-friendly version of this exact title (without changing its meaning).
    2. A compelling video description (150-200 words, engaging and informative).
    3. A list of 10 SEO-rich tags.
    4. A list of 5 relevant hashtags.
    
    Format the response as plain text like this:
    
    Optimized Title: [Your optimized title]
    
    Description:
    [Your longer, engaging description]
    
    Tags: [Comma-separated list of tags]
    
    Hashtags: [Space-separated list of hashtags]
    """

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-saba-24b",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    wait_time = 5

    for retry in range(max_retries):
        try:
            response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=15)

            if response.status_code == 200:
                content = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
                if not content:
                    print("❌ SEO Optimization Error: Empty response content")
                    return None
                
                # Parse the response
                result = {"title": "", "description": "", "tags": [], "hashtags": []}
                lines = content.split("\n")
                current_field = None

                for line in lines:
                    line = line.strip()
                    if line.startswith("Optimized Title:"):
                        result["title"] = line.replace("Optimized Title:", "").strip().strip('"')
                    elif line.startswith("Description:"):
                        current_field = "description"
                        result["description"] = line.replace("Description:", "").strip()
                    elif line.startswith("Tags:"):
                        result["tags"] = [tag.strip() for tag in line.replace("Tags:", "").split(",") if tag.strip()]
                    elif line.startswith("Hashtags:"):
                        result["hashtags"] = [tag.strip() for tag in line.replace("Hashtags:", "").split() if tag.strip()]
                    elif current_field == "description" and line:
                        result["description"] += " " + line
                
                result["description"] = result["description"].strip()
                
                # Append hashtags to title and description
                hashtags_str = " ".join(result["hashtags"][:3])  # Limit to 3 for brevity
                if result["title"]:
                    result["title"] = f"{result['title']} {hashtags_str}"
                if result["description"]:
                    result["description"] = f"{result['description']} {hashtags_str}"
                
                # Combine tags and hashtags
                result["tags"] = result["tags"] + result["hashtags"]
                
                if not result["title"]:
                    print("❌ SEO Optimization Error: No title generated")
                    return None
                    
                print(f"✅ SEO Parsed: {result}")
                return result
            
            elif response.status_code in (429, 503):
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    try:
                        wait_time = int(retry_after)
                    except ValueError:
                        wait_time = 10
                print(f"⚠️ API error [{response.status_code}]: Overloaded or rate-limited. Retrying in {wait_time}s (attempt {retry + 1}/{max_retries})")
                time.sleep(wait_time)
                wait_time = min(wait_time * 2, 60)
            
            else:
                print(f"❌ SEO Optimization Error: {response.status_code}, {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ SEO Optimization Exception: {e}")
            return None

    print(f"❌ Max retries reached for SEO API. Using fallback metadata.")
    hashtags = [f"#{video_title.replace(' ', '')}", "#video"]
    hashtags_str = " ".join(hashtags)
    return {
        "title": f"{video_title} - Auto-Generated Video {hashtags_str}",
        "description": f"Explore {video_title} in this engaging video. Learn about its key aspects and impact. Subscribe for more! {hashtags_str}",
        "tags": [video_title, f"{video_title} video", "auto-generated"] + hashtags,
        "hashtags": hashtags
    }