from models.tts_model import TTSModel

def text_to_speech(text):
    """Convert generated script to speech using gTTS."""
    tts_model = TTSModel()
    tts_model.convert_text_to_speech(text)
