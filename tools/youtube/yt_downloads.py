#!/usr/bin/env python3
"""
YouTube Audio Downloader using yt-dlp that saves to BytesIO
----------------------------------------------------------
Requirements: yt-dlp (install with 'pip install yt-dlp')
"""

import io
import os
import shutil
import tempfile

import yt_dlp


def download_youtube_audio_to_memory(url) -> tuple[io.BytesIO, str, dict]:
    """
    Download audio from a YouTube video using yt-dlp and return as BytesIO object

    Args:
        url (str): YouTube video URL

    Returns:
        tuple: (BytesIO object containing the audio, filename, info_dict)
              Returns (None, None, None) if download failed
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
        }

        print(f"Extracting audio from: {url}")

        # Download the audio to the temporary directory
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
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

            # Check if file exists (it should, but let's be safe)
            if not os.path.exists(file_path):
                # Try to find any audio file in the temp directory
                files = os.listdir(temp_dir)
                audio_files = [f for f in files if f.endswith((".mp3", ".m4a", ".webm", ".opus"))]

                if audio_files:
                    file_path = os.path.join(temp_dir, audio_files[0])
                else:
                    print("Could not find downloaded audio file")
                    return None, None, None

            # Read the file into BytesIO
            audio_bytes = io.BytesIO()
            with open(file_path, "rb") as f:
                audio_bytes.write(f.read())

            # Rewind the BytesIO object to the beginning
            audio_bytes.seek(0)

            # Get just the filename without path
            filename_only = os.path.basename(file_path)

            print(f"Successfully downloaded: {filename_only}")

            return audio_bytes, filename_only, info_dict

    except Exception as e:
        print(f"Error downloading audio: {str(e)}")
        return None, None, None

    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)


# Example usage
