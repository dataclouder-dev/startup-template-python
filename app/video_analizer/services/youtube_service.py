import io

from tools.youtube.yt_downloads import download_youtube_audio_to_memory


def download_audio(url: str) -> tuple[io.BytesIO, str, dict]:
    return download_youtube_audio_to_memory(url)
