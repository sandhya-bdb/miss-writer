from openai import OpenAI
from app.utils.config import settings

client = OpenAI(api_key=settings.openai_api_key)

def transcribe_audio(file_path: str) -> str:
    """
    Transcribe the given audio file using OpenAI's Whisper API.
    """
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
    return transcription
