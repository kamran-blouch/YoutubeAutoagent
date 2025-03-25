import requests
from configs.settings import GROQ_API_KEY

# ✅ Correct Groq API URL
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def optimize_seo(video_title):
    """
    Generates an SEO-optimized title, description, tags, and hashtags for the given video title.
    """
    prompt = f"""
    Optimize the SEO for the following YouTube video title:
    
    Title: "{video_title}"
    
    Provide:
    1. A more SEO-friendly version of this exact title (without changing its meaning).
    2. A compelling video description (150-200 words, making it engaging and informative).
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

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        else:
            print(f"❌ SEO Optimization Error: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"❌ SEO Optimization Exception: {e}")
        return None

