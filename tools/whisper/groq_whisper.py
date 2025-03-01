import os
from typing import Optional

from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def transcribe_audio_with_bytes(audio_file: bytes, model: str = "whisper-large-v3") -> Optional[str]:
    transcription = client.audio.transcriptions.create(
        file=("audio.mp3", audio_file),
        model=model,
        # prompt="Specify context or spelling",  # Optional
        response_format="verbose_json",
        # timestamp_granularities=["word"],  # Optional
    )
    print(transcription)
    return transcription


def transcribe_audio_groq(filename: str, model: str = "whisper-large-v3") -> dict:
    with open(filename, "rb") as file:
        print("Transcribing audio...", file)
        transcription = client.audio.transcriptions.create(
            file=(filename, file.read()),
            model=model,
            prompt="Specify context or spelling",  # Optional
            response_format="verbose_json",
            # timestamp_granularities=["segment"],  # Optional
            #   language="en",  # Optional
            temperature=0.0,  # Optional
        )
        print(transcription)
        return transcription
