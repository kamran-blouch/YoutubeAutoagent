import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
DEFAULT_REGION = os.getenv("DEFAULT_REGION", "US")
MAX_RESULTS = int(os.getenv("MAX_RESULTS", 5))
PEXELS_API = os.getenv("PEXELS_API")
HUGGINGFACE_API_KEY = os.getenv("Huggingface_API_KEY")



