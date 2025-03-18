from gtts import gTTS
import os

class TTSModel:
    def convert_text_to_speech(self, text):
        try:
            tts = gTTS(text=text, lang="en")
            audio_file = "output_audio.mp3"
            tts.save(audio_file)
            print(f"✅ Speech saved as {audio_file}")
            os.system(f"start {audio_file}")  # Opens the audio file automatically (Windows)
            return audio_file
        except Exception as e:
            print(f"❌ Error in TTS conversion: {e}")
