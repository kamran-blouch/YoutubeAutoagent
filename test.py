import requests
import time
from configs.settings import HUGGINGFACE_API_KEY



# API URL for Stable Diffusion
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

# Headers for authentication
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

# Define the prompt
payload = {"inputs": "girlfriend with her boyfriend"}

# Make the API request
response = requests.post(API_URL, headers=headers, json=payload)

# Handle response
if response.status_code == 200:
    # Save the image
    with open("generated_image.png", "wb") as f:
        f.write(response.content)
    print("✅ Image saved as 'generated_image.png'")
else:
    print(f"❌ Error: {response.status_code}, {response.json()}")

# Wait before making another request (due to rate limits)
time.sleep(10)
