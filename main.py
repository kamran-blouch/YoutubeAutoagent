import os
from agents.idea_generation import get_trending_ideas
from agents.script_writer import script_generator
from agents.text_to_speech import TTSModel
from agents.video_editor import create_video
from agents.subtitle_generator import add_subtitles_to_video
from configs.settings import DEFAULT_REGION, MAX_RESULTS

def main():
    """Main function to integrate all agents and generate a complete YouTube video."""
    print("\n📌 Choose how you want to generate a script for your YouTube agent:")
    print("1. Use a trending topic (from Idea Generation Agent)")
    print("2. Enter a custom topic")
    
    choice = input("\nEnter 1 or 2: ").strip()

    if choice == "1":
        region = input("\nEnter country code (e.g., US, GB, IN, PK): ").strip().upper()
        specific_topic = input("Enter a specific topic (or press Enter for general trending topics): ").strip()
        trending_ideas = get_trending_ideas(region, specific_topic if specific_topic else None, MAX_RESULTS, return_json=False)
        trending_topics = trending_ideas["trending_topics"]

        if not trending_topics:
            print("❌ No trending topics found. Try again later.")
            return

        print(f"\n📌 Trending Topics in {region} for '{specific_topic if specific_topic else 'General Trends'}':")
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

    script_result = script_generator(region if choice == "1" else DEFAULT_REGION, selected_topic, return_json=False)
    print("\n📌 Generated Video Script:")
    print(script_result)

    print("\n🎙️ Converting script to speech...")
    tts_model = TTSModel()
    audio_file = tts_model.convert_text_to_speech(script_result)
    
    if audio_file and os.path.exists(audio_file):
        print(f"\n✅ Audio generated successfully: {audio_file}")
    else:
        print("\n❌ Audio generation failed. Check TTS output.")
        return
    
    generate_video_choice = input("\n🎥 Do you want to generate a video for this script? (Press Enter to continue, or type 'no' to exit): ").strip().lower()
    
    if generate_video_choice in ["", "yes"]:
        print("\n🔍 Searching for relevant videos from Pexels...")
        video_path = create_video(selected_topic, audio_file)
        
        if video_path:
            print(f"\n✅ Video successfully generated: {video_path}")
            
            # Add subtitles to the video
            print("\n📝 Generating subtitles...")
            final_video_with_subs = add_subtitles_to_video(video_path, script_result, "final_video_with_subs.mp4")
            print(f"\n✅ Final video with subtitles generated: {final_video_with_subs}")
        else:
            print("\n❌ Failed to generate video. Please try again later.")
    
if __name__ == "__main__":
    main()
