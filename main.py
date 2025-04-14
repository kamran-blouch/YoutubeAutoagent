import os
from agents.idea_generation import get_trending_ideas
from agents.script_writer import script_generator
from agents.text_to_speech import TTSModel
from agents.video_editor import create_video
from agents.subtitle_generator import add_subtitles_to_video
from agents.thumbnail_generator import generate_thumbnail
from agents.seo_optimizer import optimize_seo
from agents.video_upload import upload_video_with_thumbnail
from configs.settings import DEFAULT_REGION, MAX_RESULTS

DEFAULT_THUMBNAIL = "default_thumbnail.png"
GENERATED_THUMBNAIL = "generated_thumbnail.png"
FINAL_VIDEO_NAME = "final_video_with_subs.mp4"

def select_from_list(prompt, options):
    print(f"\n📌 {prompt}")
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")
    try:
        idx = int(input("Enter number: ")) - 1
        if 0 <= idx < len(options):
            return options[idx]
    except ValueError:
        pass
    print("❌ Invalid selection.")
    return None

def get_topic():
    print("\n📌 Choose script generation method:\n1. Trending Topic\n2. Custom Topic")
    choice = input("Enter 1 or 2: ").strip()
    if choice == "1":
        region = input("Enter country code (e.g., US, IN): ").strip().upper()
        specific_topic = input("Enter specific topic (optional): ").strip()
        trending = get_trending_ideas(region, specific_topic or None, MAX_RESULTS, return_json=False)
        topics = trending.get("trending_topics", [])
        if not topics:
            print("❌ No trending topics found.")
            return None, None
        topic = select_from_list(f"Trending Topics in {region}", topics)
        return topic, region
    elif choice == "2":
        topic = input("Enter your custom topic: ").strip()
        return topic, DEFAULT_REGION if topic else (None, None)
    else:
        print("❌ Invalid choice.")
        return None, None

def generate_script(region, topic):
    result = script_generator(region, topic, return_json=False)
    if isinstance(result, list):
        title = select_from_list("Suggested Video Titles", result)
        return script_generator(region, title, return_json=False) if title else None
    elif isinstance(result, dict):
        if "error" in result:
            print(f"❌ Script generation failed: {result['error']}")
            return None
        return result.get("script")
    return result if isinstance(result, str) else None

def main():
    topic, region = get_topic()
    if not topic:
        return

    script = generate_script(region, topic)
    if not script or not script.strip():
        print("❌ Invalid or empty script.")
        return

    print("\n📌 Generated Script:\n", script)

    # TTS
    print("\n🎙️ Converting script to speech...")
    try:
        tts = TTSModel()
        audio_file = tts.convert_text_to_speech(script)
        if not (audio_file and os.path.exists(audio_file)):
            raise Exception("Audio file not created.")
        print(f"✅ Audio generated: {audio_file}")
    except Exception as e:
        print(f"❌ TTS Error: {e}")
        return

    # Video Generation
    if input("\n🎥 Generate video? (Enter=yes / no=skip): ").strip().lower() in ["", "yes"]:
        print("\n🔍 Searching Pexels...")
        video_path = create_video(topic, audio_file)
        if not (video_path and os.path.exists(video_path)):
            print("❌ Video generation failed.")
            return

        print(f"✅ Video created: {video_path}")
        print("\n📝 Adding subtitles...")
        final_video = add_subtitles_to_video(video_path, script, FINAL_VIDEO_NAME)
        if not final_video or not os.path.exists(final_video):
            print("❌ Subtitles failed.")
            return
        print(f"✅ Final video: {final_video}")

        # Thumbnail
        print("\n🖼️ Generating thumbnail...")
        thumb_path = generate_thumbnail(topic)
        thumb_file = GENERATED_THUMBNAIL if thumb_path and os.path.exists(GENERATED_THUMBNAIL) else None

        if not thumb_file:
            fallback = input("❌ Thumbnail failed. Use default or skip? (default/skip): ").strip().lower()
            if fallback == "default" and os.path.exists(DEFAULT_THUMBNAIL):
                if DEFAULT_THUMBNAIL != GENERATED_THUMBNAIL:
                    os.rename(DEFAULT_THUMBNAIL, GENERATED_THUMBNAIL)
                thumb_file = GENERATED_THUMBNAIL
                print(f"✅ Default thumbnail used: {thumb_file}")
            else:
                thumb_file = None

        # SEO Optimization
        print("\n📈 Optimizing SEO...")
        seo = optimize_seo(topic) or {}

        # Set defaults with validation
        seo["title"] = seo.get("title") or f"{topic.strip()} - Auto-Generated"
        seo["description"] = seo.get("description") or f"Explore {topic.strip()} in this AI-generated video!"
        seo["tags"] = seo.get("tags") or [topic.strip(), f"{topic.strip()} video", "AI", "auto-generated"]

        # Ensure title is valid
        if not seo["title"] or not seo["title"].strip():
            print("❌ Error: SEO title is missing or empty.")
            return

        print("✅ SEO:", seo)


        # Upload
        print("\n📤 Uploading to YouTube...")
        try:
            video_id = upload_video_with_thumbnail(
                file_path=final_video,
                title=seo["title"],
                description=seo["description"],
                tags=seo["tags"],
                thumbnail_path=thumb_file,
                category_id="22",
                privacy_status="public"
            )
            print(f"\n✅ Uploaded! Video ID: {video_id}")
        except Exception as e:
            print(f"\n❌ Upload error: {e}")

if __name__ == "__main__":
    main()
