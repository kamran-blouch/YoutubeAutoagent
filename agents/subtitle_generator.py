import os
import srt
import datetime
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.config import change_settings

# Ensure ImageMagick is set up correctly
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

def generate_srt(script_text, output_srt_path, video_duration):
    """Generates an SRT file with correct timing and consistent display."""
    lines = script_text.split(". ")  # Split script into sentences
    num_lines = len(lines)
    duration_per_line = video_duration / max(1, num_lines)  # Auto-adjust duration

    subtitles = []
    start_time = datetime.timedelta(seconds=0)

    for i, line in enumerate(lines):
        end_time = start_time + datetime.timedelta(seconds=duration_per_line)
        subtitles.append(srt.Subtitle(index=i + 1, start=start_time, end=end_time, content=line))
        start_time = end_time

    with open(output_srt_path, "w", encoding="utf-8") as srt_file:
        srt_file.write(srt.compose(subtitles))

    print(f"✅ Subtitles saved as '{output_srt_path}'")
    return output_srt_path


def add_subtitles_to_video(video_path, script_text, output_video_path):
    """Adds subtitles with a fixed font size, perfect timing, and proper alignment."""
    video = VideoFileClip(video_path)
    video_duration = video.duration
    srt_path = os.path.splitext(video_path)[0] + ".srt"

    # Generate SRT with accurate timing
    generate_srt(script_text, srt_path, video_duration)

    # Set a fixed large font size for better readability
    font_size = max(36, int(video.h * 0.08))  # 8% of video height
    subtitle_clips = []
    start_time = 0
    lines = script_text.split(". ")
    duration_per_line = video_duration / max(1, len(lines))  # Ensure perfect timing

    for line in lines:
        end_time = start_time + duration_per_line
        txt_clip = TextClip(
            line,
            fontsize=font_size,
            color="white",
            bg_color="black",  # Ensures readability
            size=(video.w * 0.9, None),  # Keep text width at 90% of the video width
            method="caption"  # Auto-wrap text properly
        )
        txt_clip = txt_clip.set_position(("center", "bottom")).set_start(start_time).set_duration(duration_per_line)
        subtitle_clips.append(txt_clip)
        start_time = end_time

    # Merge subtitles with video
    final_video = CompositeVideoClip([video] + subtitle_clips)
    final_video.write_videofile(output_video_path, codec="libx264", fps=video.fps)

    print(f"✅ Final video with subtitles saved as '{output_video_path}'")
    return output_video_path
