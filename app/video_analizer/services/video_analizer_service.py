import asyncio
import re

from tools.tiktok_analizer import tiktok_downloader, video_extraction


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

    if result is None:
        print(f"Could not retrieve video data for {url}")
        return

    video_bytes, storage_data = await tiktok_downloader.download_video_and_upload_to_storage(result)

    print("☁️ downloaded and uploaded to cloud", storage_data)

    # video_path = str(download_path / f"{video_id}.mp4")
    storage_frames_dir = f"tiktok/{username}/frames/{video_id}"

    storage_screnshots = video_extraction.extract_frames_and_upload(video_bytes, storage_frames_dir)
    print(" 🎞️ extracted frames", storage_frames_dir, storage_screnshots)
    print("❌ Check: save in db", storage_screnshots)
    # output_audio_dir = str(download_path / "audio")
    # audio_path = video_extraction.extract_audio(video_path, output_audio_dir)
    # print(" 🎤 extracted audio", audio_path)

    # transcription = groq_whisper.transcribe_audio_groq(audio_path)
    # transcription_text = transcription.text
    # print("transcription", transcription_text, transcription.language, transcription.segments, transcription.duration)
    # Read audio using whisper.

    # move all data to sources.


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
