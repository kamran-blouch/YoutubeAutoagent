import os
import requests
import re  # ✅ Used to clean non-spoken text
from configs.settings import GROQ_API_KEY

GROQ_MODEL = "mixtral-8x7b-32768"  # ✅ Best available model from Groq

def clean_script_for_voice(script):
    """Cleans the script by removing unwanted characters and ensuring a short, well-structured format."""
    script = re.sub(r"\[.*?\]", "", script)  # ✅ Remove scene descriptions in brackets []
    script = re.sub(r"(\bNarrator\b\s*[:\"]*)", "", script)  # ✅ Remove 'Narrator' labels and quotes
    script = re.sub(r"[{}]", "", script)  # ✅ Remove curly brackets {}
    script = re.sub(r"^\s*\"|\"\s*$", "", script)  # ✅ Remove leading/trailing double quotes
    script = re.sub(r"[^\w\s.,'!?]", "", script)  # ✅ Keep only normal punctuation
    script = re.sub(r"\s+", " ", script).strip()  # ✅ Normalize spaces

    # ✅ Remove "Total word count..." and similar phrases
    script = re.sub(r"Total word count.*", "", script, flags=re.IGNORECASE).strip()

    # ✅ Limit script to ~30 seconds (about 75 words)
    words = script.split()
    if len(words) > 75:
        script = " ".join(words[:75]) + "..."  # ✅ Truncate if too long

    return script






def generate_titles(topic):
    """Generate 5 specific video titles for the given topic using Groq API."""
    prompt_message = [
        {"role": "system", "content": "You are an expert YouTube content strategist."},
        {"role": "user", "content": f"Generate exactly 5 unique, trending, and engaging YouTube video titles about {topic}. Return each title as a separate line."}
    ]

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
        json={"model": GROQ_MODEL, "messages": prompt_message, "max_tokens": 200}
    )

    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip().split("\n")

    return ["Error fetching titles from Groq API"]

def generate_script(title):
    """Generate a fully dynamic video script for the selected title using Groq API."""
    prompt_message = [
        {"role": "user", "content": f"""Write a complete and engaging 30-second YouTube script for the title: '{title}'.
Make sure it covers all key details in a short and impactful way, like a viral YouTube Short.
Use concise sentences, avoid unnecessary repetition, and provide a clear summary of the topic in 70-80 words."""}
    ]

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
        json={"model": GROQ_MODEL, "messages": prompt_message, "max_tokens": 300}
    )

    if response.status_code == 200:
        raw_script = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        return clean_script_for_voice(raw_script)  # ✅ Ensures only spoken words are returned

    return "Error generating script from Groq API"
