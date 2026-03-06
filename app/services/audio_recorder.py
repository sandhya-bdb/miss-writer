import sounddevice as sd
import soundfile as sf
import logging

logger = logging.getLogger(__name__)

def record_audio(filename: str, duration: int = 10, fs: int = 44100) -> str:
    """
    Record audio from the microphone for a specified duration and save it to a file.
    Note: Primarily used for CLI testing. Web app uses client-side recording.
    """
    logger.info(f"Recording for {duration} seconds to {filename}...")
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    logger.info("Recording finished!")
    sf.write(filename, myrecording, fs)
    return filename
