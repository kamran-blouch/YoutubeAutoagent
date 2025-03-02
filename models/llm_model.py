import os
import requests
import re  # ✅ Used to clean non-spoken text
from configs.settings import GROQ_API_KEY

GROQ_MODEL = "mixtral-8x7b-32768"  # ✅ Best available model from Groq

def clean_script_for_voice(script):
    """Removes scene directions (brackets) so the voice generator only gets spoken text."""
    script = re.sub(r"\[.*?\]", "", script).strip()  # ✅ Remove scene descriptions
    script = re.sub(r"\n{3,}", "\n\n", script)  # ✅ Ensure only two newlines for proper spacing
    script = script.replace(". .", ".")  # ✅ Remove extra periods caused by previous replacements
    script = re.sub(r"\bNarrator:\s*", "", script)  # ✅ Remove "Narrator:" and extra spaces
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
        {"role": "system", "content": "You are a professional scriptwriter who generates human-like, engaging YouTube scripts."},
        {"role": "user", "content": f"Write a detailed, engaging 30-second YouTube script for the title: '{title}'. Keep it topic-specific and highly engaging."}
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
