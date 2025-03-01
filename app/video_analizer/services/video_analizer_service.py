import asyncio
import re

from app.agents.models.agent_sources_model import AgentSource, ImageSource, SourceType, VideoSource
from app.agents.repositories import agent_sources_repository
from tools.tiktok_analizer import tiktok_downloader, video_extraction
from tools.whisper import groq_whisper


async def analize_video(url: str) -> None:
    await download_tiktok_upload_files_and_update_db(url)


async def save_tiktok_data(urls: list[str]) -> None:
    for ind, url in enumerate(urls):
        print(f"* {ind + 1}/{len(urls)} Getting data from video: {url}")
        username, video_id = extract_tiktok_url_components(url)
        data = await tiktok_downloader.request_data(video_id)
        saved_id = tiktok_downloader.save_in_db(data)
        await asyncio.sleep(0.7)
        print("saved tiktok data", saved_id)


async def download_tiktok_upload_files_and_update_db(url: str) -> None:
    # This function only download video in memory, not save in disk.
    username, video_id = extract_tiktok_url_components(url)
    print(f" 🎞️ Starting download username: {username}, video_id: {video_id}")
    result = await tiktok_downloader.get_video(url)

    agent_source = AgentSource(type=SourceType.TIKTOK)

    print(" * 1) downloading video and uploading to cloud")
    video_bytes = await tiktok_downloader.download_tiktok_media(result)

    video_storage_ref = f"tiktok/{username}/videos/{video_id}.mp4"
    storage_data = await tiktok_downloader.upload_media_to_storage(video_storage_ref, video_bytes)
    print("☁️ downloaded and uploaded to cloud", storage_data)
    video_source = VideoSource(idPlatform=video_id, video=storage_data)
    agent_source.video = video_source
    agent_source = agent_sources_repository.save_source(agent_source)
    print("🔍 saved in db", agent_source)

    print(" * 2) extracting frames and uploading to cloud")

    storage_frames_dir = f"tiktok/{username}/frames/{video_id}"
    screenshots = video_extraction.extract_frames_from_video_bytes(video_bytes)
    print("🖼️ extracted screenshots", len(screenshots))
    storage_screnshots = video_extraction.upload_frames_to_storage(screenshots, storage_frames_dir)
    print("Ready to save in db", storage_screnshots)
    video_frames = [ImageSource(image=frame, description="", title="") for frame in storage_screnshots]
    agent_source.video.frames = video_frames
    agent_source = agent_sources_repository.save_source(agent_source)

    print(" * 3) Extract Audio and Transcription")
    audio_bytes = video_extraction.extract_audio_from_video_bytes(video_bytes)
    audio_storage_ref = f"tiktok/{username}/audio/{video_id}.mp3"
    audio_storage_data = await tiktok_downloader.upload_media_to_storage(audio_storage_ref, audio_bytes)
    print("🎤 extracted audio, uploaded to cloud and starting transcription", audio_storage_data)

    transcription = groq_whisper.transcribe_audio_with_bytes(audio_bytes)
    transcription_object = {"text": transcription.text, "language": transcription.language, "segments": transcription.segments, "duration": transcription.duration}
    print("🎤 transcription", transcription_object)
    agent_source.video.transcription = transcription_object
    agent_source = agent_sources_repository.save_source(agent_source)
    print("Process completed", agent_source)
    return agent_source


def extract_tiktok_url_components(url: str) -> tuple[str, str]:
    """
    Extract username and video ID from a TikTok URL.

    Args:
        url (str): TikTok video URL in format 'https://www.tiktok.com/@username/video/videoid'

    Returns:
        tuple[str, str]: A tuple containing (username, video_id)

    Raises:
        ValueError: If the URL format is invalid
    """
    match = re.match(r"https://(?:www\.)?tiktok\.com/@([^/]+)/video/(\d+)", url)
    if not match:
        raise ValueError("Invalid TikTok URL format")

    username = match.group(1)
    video_id = match.group(2)

    return username, video_id


def get_tiktok_sources(video_id: str) -> list[dict]:
    return agent_sources_repository.find_sources_by_video_platform_id(video_id)
