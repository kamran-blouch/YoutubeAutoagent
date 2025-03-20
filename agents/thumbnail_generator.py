import requests
import time
from configs.settings import HUGGINGFACE_API_KEY

API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def generate_thumbnail(prompt, output_path="generated_thumbnail.png", max_retries=5):
    """Generates a thumbnail using Hugging Face API with retries and backoff."""
    payload = {"inputs": prompt}
    wait_time = 5  # Initial backoff time (seconds)

    for retry in range(max_retries):
        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload)

            if response.status_code == 200 and response.content:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                print(f"✅ Thumbnail saved: {output_path}")
                return output_path

            elif response.status_code == 503:
                print(f"⚠️ API overloaded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                wait_time *= 2  # Slowly increase wait time
            
            else:
                error_message = response.text if not response.content else response.json()
                print(f"❌ API Error [{response.status_code}]: {error_message}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"❌ Request Error: {e}")
            return None

    print("❌ Max retries reached. Thumbnail generation failed.")
    return None
