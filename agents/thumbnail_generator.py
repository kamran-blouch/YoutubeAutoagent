import os
import requests
from configs.settings import HUGGINGFACE_API_KEY

def generate_thumbnail(topic: str) -> str | None:
    """Generates a new thumbnail for the topic."""
    output_path = "generated_thumbnail.png"
    
    # Delete existing thumbnail
    if os.path.exists(output_path):
        os.remove(output_path)
    
    # Call Hugging Face API (example)
    url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": f"A vibrant YouTube thumbnail for {topic}"}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            if os.path.exists(output_path):
                print("✅ New thumbnail generated.")
                return output_path
        print(f"❌ Thumbnail API error: {response.status_code}")
    except Exception as e:
        print(f"❌ Thumbnail error: {e}")
    
    return None