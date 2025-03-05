from agents.idea_generation import get_trending_ideas
from agents.script_writer import script_generator
from agents.text_to_speech import text_to_speech
from configs.settings import DEFAULT_REGION, MAX_RESULTS

def main():
    """Main function to integrate Idea Generation, Script Generator, and TTS Agents."""
    
    print("\n📌 Choose how you want to generate a script for your YouTube agent:")
    print("1. Use a trending topic (from Idea Generation Agent)")
    print("2. Enter a custom topic")
    
    choice = input("\nEnter 1 or 2: ").strip()

    if choice == "1":
        # Ask for region input
        region = input("\nEnter country code (e.g., US, GB, IN, PK): ").strip().upper()
        specific_topic = input("Enter a specific topic (or press Enter for general trending topics): ").strip()

        # Fetch trending topics based on user input
        trending_ideas = get_trending_ideas(region, specific_topic if specific_topic else None, MAX_RESULTS, return_json=False)
        trending_topics = trending_ideas["trending_topics"]

        if not trending_topics:
            print("❌ No trending topics found. Try again later.")
            return

        print("\n📌 Trending Topics in", region, f"for '{specific_topic if specific_topic else 'General Trends'}':")
        for idx, topic in enumerate(trending_topics, start=1):
            print(f"{idx}. {topic}")

        try:
            selected_index = int(input("\nSelect a topic by number: ")) - 1
            if selected_index < 0 or selected_index >= len(trending_topics):
                print("❌ Invalid selection.")
                return
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            return

        selected_topic = trending_topics[selected_index]
        print(f"\n✅ Selected Topic: {selected_topic}")

    elif choice == "2":
        selected_topic = input("\nEnter your custom topic: ").strip()
        if not selected_topic:
            print("❌ Invalid input. Topic cannot be empty.")
            return
    else:
        print("❌ Invalid choice. Please enter 1 or 2.")
        return

    # Generate script for the selected topic
    script_result = script_generator(region if choice == "1" else DEFAULT_REGION, selected_topic, return_json=True)
    
    print("\n📌 Generated Video Script:")
    print(script_result)

    # Convert script to speech
    print("\n🎙️ Converting script to speech...")
    text_to_speech(script_result)

if __name__ == "__main__":
    main()
