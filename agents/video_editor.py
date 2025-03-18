import os
import requests
import tempfile
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from models.vision_model import search_videos_on_pexels


def stream_video(url):
    """
    Streams a video file from a URL and returns the local temp file path.
    """
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
                temp_file.write(chunk)
            return temp_file.name
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to stream video from {url}: {e}")
        return None

def create_video(topic, audio_file):
    """
    Creates a final video using multiple clips streamed from Pexels.
    """
    print(f"🔍 Searching for videos related to: {topic}")
    video_urls = search_videos_on_pexels(topic, num_results=7)
    
    if not video_urls:
        print("❌ No relevant videos found.")
        return None
    
    video_clips = []
    temp_files = []  # Track temp files for cleanup
    
    for url in video_urls:
        video_path = stream_video(url)
        if video_path:
            try:
                clip = VideoFileClip(video_path)
                subclip_duration = min(3, clip.duration)
                resized_clip = clip.subclip(0, subclip_duration).resize((1920, 1080))
                video_clips.append(resized_clip)
                temp_files.append(video_path)  # Store for cleanup
            except Exception as e:
                print(f"⚠️ Error processing video: {e}")
    
    if not video_clips:
        print("❌ No valid video clips found.")
        return None
    
    # Load the audio clip
    audio_clip = AudioFileClip(audio_file)
    audio_duration = audio_clip.duration  # Get the duration of the audio
    
    # Repeat the video clips until they match the audio duration
    final_clips = []
    current_duration = 0
    clip_index = 0
    
    while current_duration < audio_duration:
        clip = video_clips[clip_index % len(video_clips)]  # Loop through videos if needed
        final_clips.append(clip)
        current_duration += clip.duration
        clip_index += 1
    
    # Merge all selected clips
    final_video = concatenate_videoclips(final_clips, method="compose").set_audio(audio_clip)
    
    # Save the final video
    output_video = "final_video.mp4"
    final_video.write_videofile(output_video, codec="libx264", fps=24, audio_codec="aac", threads=4)
    
    # Cleanup temporary video files
    for clip in video_clips:
        clip.close()
    
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
            
        except Exception as e:
            print(f"⚠️ Failed to delete temp file {temp_file}: {e}")
    
    return output_video
