import asyncio
import re

from app.agents.models.agent_sources_model import AgentSource, ImageSource, SourceType, VideoSource
from app.agents.repositories import agent_sources_repository
from app.video_analizer.models.model import VideoAnalysisModel
from tools.tiktok_analizer import tiktok_downloader, video_extraction
from tools.whisper import groq_whisper
from tools.youtube import yt_dlp_utils


def save_agent_source() -> AgentSource:
    agent_source = AgentSource(type=SourceType.TIKTOK, status="processing", statusDescription="Extracting tiktok data...")
    return agent_sources_repository.save_source(agent_source)


async def analize_video(videoAnalysis: VideoAnalysisModel, agent_source: AgentSource) -> AgentSource:
    # Run the potentially blocking operation in a thread pool
    # This prevents it from blocking the event loop
    if videoAnalysis.website == "tiktok":
        asyncio.create_task(_run_analysis(videoAnalysis.url, agent_source))
    elif videoAnalysis.website == "youtube":
        asyncio.create_task(_run_analysis_youtube(videoAnalysis.url, agent_source))
    else:
        raise ValueError("Invalid website")

    return agent_source


async def _run_analysis_youtube(url: str, agent_source: AgentSource) -> None:
    try:
        await download_youtube_video_upload_files_and_update_db(url, agent_source)
    except Exception as e:
        print(f"Error in background analysis: {e}")
        _save_source_status(agent_source, f"Error during analysis: {str(e)}")
        agent_sources_repository.save_source(agent_source)


async def _run_analysis(url: str, agent_source: AgentSource) -> None:
    try:
        await download_tiktok_upload_files_and_update_db(url, agent_source)
    except Exception as e:
        print(f"Error in background analysis: {e}")
        _save_source_status(agent_source, f"Error during analysis: {str(e)}")
        agent_sources_repository.save_source(agent_source)


async def save_tiktok_data(urls: list[str]) -> None:
    for ind, url in enumerate(urls):
        print(f"* {ind + 1}/{len(urls)} Getting data from video: {url}")
        username, video_id = extract_tiktok_url_components(url)
        data = await tiktok_downloader.request_data(video_id)
        saved_id = tiktok_downloader.save_in_db(data)
        await asyncio.sleep(0.7)
        print("saved tiktok data", saved_id)


async def download_youtube_video_upload_files_and_update_db(url: str, agent_source: AgentSource) -> None:
    # Todo check if this method is working...r
    video_bytes, info_dict = yt_dlp_utils.download_youtube_video_to_memory(url)
    video_storage_ref = f"youtube/{info_dict.get('id', 'video')}.mp4"
    _save_source_status(agent_source, "Uploading video to cloud storage...")
    # Refactor this, i need stourage libs with this method
    storage_data = await tiktok_downloader.upload_media_to_storage(video_storage_ref, video_bytes)
    _save_source_status(agent_source, "Video uploaded to cloud storage! Saving database..." + str(storage_data))
    agent_source.video = VideoSource(idPlatform=info_dict.get("id", "video"), video=storage_data)
    agent_source = agent_sources_repository.save_source(agent_source)
    pass


async def download_tiktok_upload_files_and_update_db(url: str, agent_source: AgentSource) -> None:
    # 2. Extract tiktok data
    username, video_id = extract_tiktok_url_components(url)
    _save_source_status(agent_source, f"Extracting tiktok video data, id {video_id} from username: {username}...")

    parsed_data, tiktok_data = await tiktok_downloader.get_titktok_video_data(url)
    agent_source.relationId = parsed_data.get("id")
    # Donwload video
    agent_source.name = tiktok_data.get("author", {}).get("nickname") + " - " + tiktok_data.get("desc")[0:20]
    agent_source.description = tiktok_data.get("desc")
    _save_source_status(agent_source, "Tiktok Video Found! Downloading video...")
    video_bytes = await tiktok_downloader.download_tiktok_media(parsed_data)

    # Upload video to cloud
    _save_source_status(agent_source, "Uploading video to cloud storage...")
    video_storage_ref = f"tiktok/{username}/videos/{video_id}.mp4"
    storage_data = await tiktok_downloader.upload_media_to_storage(video_storage_ref, video_bytes)
    # Save video source
    _save_source_status(agent_source, "Video uploaded to cloud storage! Saving database..." + str(storage_data))
    video_source = VideoSource(idPlatform=video_id, video=storage_data)
    agent_source.video = video_source
    agent_source = agent_sources_repository.save_source(agent_source)

    # Extract Images frames.
    _save_source_status(agent_source, "Extracting frames from video...")

    storage_frames_dir = f"tiktok/{username}/frames/{video_id}"
    screenshots = video_extraction.extract_frames_from_video_bytes(video_bytes)

    # Upload frames to cloud
    _save_source_status(agent_source, f"Uploading {len(screenshots)} frames to cloud storage...")
    storage_screnshots = video_extraction.upload_frames_to_storage(screenshots, storage_frames_dir)
    video_frames = [ImageSource(image=frame, description="", title="") for frame in storage_screnshots]
    agent_source.video.frames = video_frames

    # Extracting and uploading audio
    _save_source_status(agent_source, "Extracting audio from video...")
    audio_bytes = video_extraction.extract_audio_from_video_bytes(video_bytes)
    audio_storage_ref = f"tiktok/{username}/audio/{video_id}.mp3"
    audio_storage_data = await tiktok_downloader.upload_media_to_storage(audio_storage_ref, audio_bytes)
    agent_source.video.audio = audio_storage_data
    # Starting transcription.
    _save_source_status(agent_source, "Audio Extracted,  starting transcription" + str(audio_storage_data))

    transcription = groq_whisper.transcribe_audio_with_bytes(audio_bytes)
    transcription_object = {"text": transcription.text, "language": transcription.language, "segments": transcription.segments, "duration": transcription.duration}
    _save_source_status(agent_source, "🎤 transcription" + str(transcription_object))
    agent_source.video.transcription = transcription_object

    # Process completed
    _save_source_status(agent_source, "Process completed")
    return agent_source


def _save_source_status(agent_source: AgentSource, status_description: str) -> AgentSource:
    agent_source.statusDescription = status_description
    print(agent_source.statusDescription)
    agent_source = agent_sources_repository.save_source(agent_source)
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
