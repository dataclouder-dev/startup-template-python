#!/usr/bin/env python3
"""
YouTube Downloader using yt-dlp that saves to memory
---------------------------------------------------
This module provides functions to download YouTube videos and audio directly to memory
as BytesIO objects instead of writing to disk.

Example usage:
    video_bytes, video_info = download_youtube_video_to_memory("https://www.youtube.com/watch?v=example")
    audio_bytes, audio_info = download_youtube_audio_to_memory("https://www.youtube.com/watch?v=example")
"""

import io
import os
import shutil
import tempfile
from typing import Optional

# Import YoutubeDL directly from yt_dlp
from yt_dlp import YoutubeDL


def download_youtube_video_to_memory(url: str) -> tuple[Optional[io.BytesIO], Optional[dict]]:
    """
    Download a YouTube video using yt-dlp and return it as a BytesIO object.

    Args:
        url (str): YouTube video URL

    Returns:
        Tuple[Optional[io.BytesIO], Optional[Dict]]:
            - BytesIO object containing the video data
            - Info dictionary with metadata about the video
            - Returns (None, None) if download failed
    """
    # Create a temporary directory to store the file temporarily
    temp_dir = tempfile.mkdtemp()

    try:
        # Configure yt-dlp options to download to temp directory
        ydl_opts = {
            "format": "best",  # Best quality video
            "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
            "quiet": False,
            "no_warnings": False,
            "ignoreerrors": False,
            "noplaylist": True,  # Only download the video, not the playlist
        }

        print(f"Downloading video from: {url}")

        # Download the video to the temporary directory
        with YoutubeDL(ydl_opts) as ydl:
            # Extract info and download
            info_dict = ydl.extract_info(url, download=True)

            # Get the filename
            if "entries" in info_dict:  # It's a playlist
                info_dict = info_dict["entries"][0]

            # Get original filename template
            filename = ydl.prepare_filename(info_dict)

            # Full path to the downloaded file
            file_path = os.path.join(temp_dir, os.path.basename(filename))

            # Check if file exists
            if not os.path.exists(file_path):
                # Try to find any video file in the temp directory
                files = os.listdir(temp_dir)
                if files:
                    file_path = os.path.join(temp_dir, files[0])
                else:
                    print("Could not find downloaded video file")
                    return None, None

            # Read the file into BytesIO
            video_bytes = io.BytesIO()
            with open(file_path, "rb") as f:
                video_bytes.write(f.read())

            # Rewind the BytesIO object to the beginning
            video_bytes.seek(0)

            # Get just the filename without path
            filename_only = os.path.basename(file_path)

            print(f"Successfully downloaded: {filename_only}")

            return video_bytes, info_dict

    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return None, None

    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)


def download_youtube_audio_to_memory(url: str) -> tuple[Optional[io.BytesIO], Optional[dict]]:
    """
    Download audio from a YouTube video using yt-dlp and return as BytesIO object.

    Args:
        url (str): YouTube video URL

    Returns:
        Tuple[Optional[io.BytesIO], Optional[Dict]]:
            - BytesIO object containing the audio data
            - Info dictionary with metadata about the audio
            - Returns (None, None) if download failed
    """
    # Create a temporary directory to store the file temporarily
    temp_dir = tempfile.mkdtemp()

    try:
        # Configure yt-dlp options to download to temp directory
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
            "quiet": False,
            "no_warnings": False,
            "ignoreerrors": False,
            "noplaylist": True,  # Only download the video, not the playlist
        }

        print(f"Extracting audio from: {url}")

        # Download the audio to the temporary directory
        with YoutubeDL(ydl_opts) as ydl:
            # Extract info and download
            info_dict = ydl.extract_info(url, download=True)

            # Get the filename
            if "entries" in info_dict:  # It's a playlist
                info_dict = info_dict["entries"][0]

            # Get original filename template
            filename = ydl.prepare_filename(info_dict)

            # Change extension to mp3 since FFmpeg post-processor converts it
            base_filename = os.path.splitext(filename)[0]
            mp3_filename = base_filename + ".mp3"

            # Full path to the downloaded file
            file_path = os.path.join(temp_dir, os.path.basename(mp3_filename))

            # Check if file exists
            if not os.path.exists(file_path):
                # Try to find any audio file in the temp directory
                files = os.listdir(temp_dir)
                audio_files = [f for f in files if f.endswith((".mp3", ".m4a", ".webm", ".opus"))]

                if audio_files:
                    file_path = os.path.join(temp_dir, audio_files[0])
                else:
                    print("Could not find downloaded audio file")
                    return None, None

            # Read the file into BytesIO
            audio_bytes = io.BytesIO()
            with open(file_path, "rb") as f:
                audio_bytes.write(f.read())

            # Rewind the BytesIO object to the beginning
            audio_bytes.seek(0)

            print(f"Successfully downloaded audio: {os.path.basename(file_path)}")

            return audio_bytes, info_dict

    except Exception as e:
        print(f"Error downloading audio: {str(e)}")
        return None, None

    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)


def download_youtube_audio_with_format(url: str, audio_format: str = "mp3", audio_quality: str = "192") -> tuple[Optional[io.BytesIO], Optional[dict]]:
    """
    Download audio from a YouTube video with specified format and quality.

    Args:
        url (str): YouTube video URL
        audio_format (str): Audio format (mp3, m4a, wav, etc.)
        audio_quality (str): Audio quality (bitrate, e.g., "192", "256", "320")

    Returns:
        Tuple[Optional[io.BytesIO], Optional[Dict]]:
            - BytesIO object containing the audio data
            - Info dictionary with metadata about the audio
            - Returns (None, None) if download failed
    """
    # Create a temporary directory to store the file temporarily
    temp_dir = tempfile.mkdtemp()

    try:
        # Configure yt-dlp options to download to temp directory
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": audio_format,
                    "preferredquality": audio_quality,
                }
            ],
            "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
            "quiet": False,
            "no_warnings": False,
            "ignoreerrors": False,
            "noplaylist": True,  # Only download the video, not the playlist
        }

        print(f"Extracting {audio_format} audio from: {url}")

        # Download the audio to the temporary directory
        with YoutubeDL(ydl_opts) as ydl:
            # Extract info and download
            info_dict = ydl.extract_info(url, download=True)

            # Get the filename
            if "entries" in info_dict:  # It's a playlist
                info_dict = info_dict["entries"][0]

            # Get original filename template
            filename = ydl.prepare_filename(info_dict)

            # Change extension to the specified audio format
            base_filename = os.path.splitext(filename)[0]
            audio_filename = base_filename + f".{audio_format}"

            # Full path to the downloaded file
            file_path = os.path.join(temp_dir, os.path.basename(audio_filename))

            # Check if file exists
            if not os.path.exists(file_path):
                # Try to find any audio file in the temp directory
                files = os.listdir(temp_dir)
                audio_files = [f for f in files if f.endswith(f".{audio_format}") or f.endswith((".m4a", ".webm", ".opus"))]

                if audio_files:
                    file_path = os.path.join(temp_dir, audio_files[0])
                else:
                    print("Could not find downloaded audio file")
                    return None, None

            # Read the file into BytesIO
            audio_bytes = io.BytesIO()
            with open(file_path, "rb") as f:
                audio_bytes.write(f.read())

            # Rewind the BytesIO object to the beginning
            audio_bytes.seek(0)

            print(f"Successfully downloaded audio: {os.path.basename(file_path)}")

            return audio_bytes, info_dict

    except Exception as e:
        print(f"Error downloading audio: {str(e)}")
        return None, None

    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)


def download_youtube_video_and_audio(url: str) -> tuple[Optional[io.BytesIO], Optional[io.BytesIO], Optional[dict]]:
    """
    Download both video and audio from a YouTube URL and return them as BytesIO objects.

    Args:
        url (str): YouTube video URL

    Returns:
        Tuple[Optional[io.BytesIO], Optional[io.BytesIO], Optional[Dict]]:
            - BytesIO object containing the video data
            - BytesIO object containing the audio data
            - Info dictionary with metadata
            - Any element can be None if that part of the download failed
    """
    video_bytes, video_info = download_youtube_video_to_memory(url)
    audio_bytes, _ = download_youtube_audio_to_memory(url)

    return video_bytes, audio_bytes, video_info


# Example usage
if __name__ == "__main__":
    # Example URL - using a clean URL without playlist parameters
    url = "https://www.youtube.com/watch?v=ltybWRg4r1c"

    # Download both video and audio
    video_bytes, audio_bytes, info = download_youtube_video_and_audio(url)

    if video_bytes and audio_bytes:
        print(f"Video size: {len(video_bytes.getvalue())} bytes")
        print(f"Audio size: {len(audio_bytes.getvalue())} bytes")
        print(f"Title: {info.get('title', 'Unknown')}")

        # Example of downloading with specific format
        mp3_bytes, _ = download_youtube_audio_with_format(url, audio_format="mp3", audio_quality="320")
        if mp3_bytes:
            print(f"High quality MP3 size: {len(mp3_bytes.getvalue())} bytes")
    else:
        print("Download failed")
