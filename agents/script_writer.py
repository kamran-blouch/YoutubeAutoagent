import json
from models.llm_model import generate_titles, generate_script
from configs.settings import DEFAULT_REGION, MAX_RESULTS

def script_generator(region=DEFAULT_REGION, topic=None, return_json=True, selected_index=None):
    """Generates a short, clean, and properly formatted video script."""

    # Step 1: Generate 5 specific video titles for the given topic
    generated_titles = generate_titles(topic)
    
    if not generated_titles or len(generated_titles) < 5:
        return {"error": "Could not generate enough specific titles for the topic."}

    if selected_index is None:  # Only ask for user input if not provided (manual run)
        for idx, title in enumerate(generated_titles, start=1):
            print(f"{title}")

        try:
            selected_index = int(input("\nEnter the number of your chosen title: ")) - 1
            if selected_index < 0 or selected_index >= len(generated_titles):
                return {"error": "Invalid selection."}
        except ValueError:
            return {"error": "Invalid input. Please enter a number."}

    selected_title = generated_titles[selected_index]

    # ✅ Generate a fully dynamic script using the Groq API
    generated_script = generate_script(selected_title)

    result = {
        "script": generated_script.strip()  # ✅ Clean, natural English script
    }

    return generated_script.strip()  # ✅ Directly return text, not JSON

