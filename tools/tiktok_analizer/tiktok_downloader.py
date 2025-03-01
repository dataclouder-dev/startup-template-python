import json
import logging
import os
from typing import TypedDict, Union

import requests

from app.modules.mongo.mongo import db
from app.storage import storage
from app.storage.storage_models import CloudStorageDataDict


class VideoSourceData(TypedDict):
    url: str  # video url from storage, don't confuse with platform url, is the source url video
    images: list[str]
    id: str


def log_retry(url: str) -> None:
    """Log URL to retry.txt when rate limit is triggered"""
    print("Logging retry")
    with open("retry.txt", "a") as f:
        f.write(f"{url}\n")


def get_id_video(url: str) -> str:
    """Extract video ID from TikTok URL"""
    print("Getting id video")
    if "/t/" in url:
        # Handle redirects for /t/ URLs if needed
        response = requests.get(url, allow_redirects=True)
        url = response.url

    video_identifier = "/video/"
    photo_identifier = "/photo/"

    if photo_identifier in url:
        id_video = url[url.find(photo_identifier) + len(photo_identifier) : url.find(photo_identifier) + len(photo_identifier) + 19]
    elif video_identifier in url:
        id_video = url[url.find(video_identifier) + len(video_identifier) : url.find(video_identifier) + len(video_identifier) + 19]
    else:
        raise ValueError("URL format not recognized")

    # Clean up ID if it contains query parameters
    if "?" in id_video:
        id_video = id_video[: id_video.find("?")]

    return id_video


def _parse_media_urls(aweme: dict, watermark: bool = False) -> tuple[str, list]:
    """Extract media URLs from aweme object"""
    url_media = ""
    image_urls = []

    if aweme.get("image_post_info"):
        print("tiktok is slideshow images")
        logging.info("Video is slideshow")
        for element in aweme["image_post_info"]["images"]:
            image_urls.append(element["display_image"]["url_list"][1])
    elif aweme.get("video"):
        print("Tiktok is video")
        video = aweme["video"]
        url_media = None

        if watermark and video.get("download_addr", {}).get("url_list"):
            url_media = video["download_addr"]["url_list"][0]

        if url_media is None and video.get("play_addr", {}).get("url_list"):
            url_media = video["play_addr"]["url_list"][0]

        if not url_media:
            logging.error("Error: video download_addr or play_addr or their url_list is missing.")
    else:
        logging.error("Error: video or image_post_info is missing in the aweme object.")

    return url_media, image_urls


async def request_data(id_video: str) -> dict:
    api_url = f"https://api22-normal-c-alisg.tiktokv.com/aweme/v1/feed/?aweme_id={id_video}&iid=7318518857994389254&device_id=7318517321748022790&channel=googleplay&app_name=musical_ly&version_code=300904&device_platform=android&device_type=ASUS_Z01QD&version=9"

    try:
        response = requests.options(api_url)
        try:
            res = json.loads(response.text)
        except json.JSONDecodeError as err:
            logging.error(f"Error parsing JSON: {err}")
            logging.error(f"Response body: {response.text}")
            if "ratelimit triggered" in response.text:
                log_retry(api_url)
            return None
        tiktok_data = res["aweme_list"][0]
        return tiktok_data
    except Exception as e:
        logging.error(f"Error fetching video: {e}")
        return None


async def get_video(url: str, watermark: bool = False) -> dict:
    """
    Fetch video information from TikTok API

    Args:
        url (str): TikTok video URL
        watermark (bool): Whether to get version with watermark

    Returns:
        dict: Contains video URL or image URLs and video ID
        Format: {
            'url': str,  # Video URL if video
            'images': list,  # List of image URLs if slideshow
            'id': str  # Video/Post ID
        }
    """
    id_video = get_id_video(url)
    print("Getting api url", id_video)

    try:
        tiktok_data = await request_data(id_video)
        save_in_db(tiktok_data)

        url_media, image_urls = _parse_media_urls(tiktok_data, watermark)
        return {"url": url_media, "images": image_urls, "id": id_video}

    except Exception as e:
        logging.error(f"Error fetching video: {e}")
        return None


def remove_from_retry(url: str) -> None:
    """Remove a URL from retry.txt after successful download"""
    try:
        print("Removing from retry")
        if not os.path.exists("retry.txt"):
            return

        with open("retry.txt") as f:
            urls = f.read().splitlines()

        urls = [u for u in urls if u != url]

        with open("retry.txt", "w") as f:
            f.write("\n".join(urls))
    except Exception as e:
        logging.error(f"Error removing URL from retry file: {e}")


def download_video(data: dict, folder: str = None, to_memory: bool = False) -> Union[None, bytes]:
    """
    Download a video from the given URL and either save it to disk or return as bytes.

    Args:
        data (dict): Dictionary containing video data with 'id' and 'url' keys
        folder (str, optional): Directory to save the video if downloading to disk. Required if to_memory is False
        to_memory (bool): If True, return video as bytes. If False, save to disk

    Returns:
        Union[None, bytes]: If to_memory is True, returns video bytes. Otherwise returns None
    """
    if not to_memory and not folder:
        raise ValueError("folder must be specified when downloading to disk")

    # Download video
    response = requests.get(data["url"], stream=True)
    response.raise_for_status()

    if to_memory:
        # Download to memory
        video_bytes = b""
        for chunk in response.iter_content(chunk_size=8192):
            video_bytes += chunk
        logging.info("Video downloaded to memory successfully")
        return video_bytes
    else:
        # Download to disk
        filename = f"{data['id']}.mp4"
        filepath = os.path.join(folder, filename)

        # Skip if file already exists
        if os.path.exists(filepath):
            logging.warning(f"File '{filename}' already exists. Skipping.")
            return None

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        logging.info("Video downloaded to disk successfully")
        return None


def download_image(data: VideoSourceData, folder: str) -> None:
    logging.info("Downloading slideshow")

    for index, image_url in enumerate(data["images"]):
        filename = f"{data['id']}_{index}.jpeg"
        filepath = os.path.join(folder, filename)

        # Skip if file already exists
        if os.path.exists(filepath):
            logging.warning(f"File '{filename}' already exists. Skipping.")
            continue

        # Download image
        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    logging.info("Slideshow downloaded successfully")


async def download_tiktok_media(data: VideoSourceData) -> bytes | None:
    """
    Download TikTok media (video or slideshow) and return the bytes

    Args:
        data (VideoSourceData): Dictionary containing media information
            Format: {
                'url': str,  # Video URL if video
                'images': list,  # List of image URLs if slideshow
                'id': str  # Video/Post ID
            }

    Returns:
        bytes | None: The downloaded video bytes if successful, None otherwise
    """
    try:
        if data.get("images"):
            print("There are images, Not support for images yet.")
            return None
        elif data["url"]:
            bytes_video = download_video(data, None, to_memory=True)
            if isinstance(bytes_video, bytes):
                return bytes_video
        else:
            logging.error("No media URL found in data")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading media: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error while downloading media: {e}")
        raise


async def upload_media_to_storage(storage_ref: str, media_bytes: bytes) -> CloudStorageDataDict | None:
    """
    Upload media bytes to storage

    Args:
        storage_ref (str): The path to save the media in storage, should include extension example: folder1/video/filename.mp4
        media_bytes (bytes): The media content to upload

    Returns:
        CloudStorageDataDict | None: Storage data if upload successful, None otherwise
    """
    try:
        storage_data = storage.upload_bytes_to_ref(storage_ref, media_bytes)
        print("Storage data", storage_data)
        return storage_data
    except Exception as e:
        logging.error(f"Error uploading media to storage: {e}")
        return None


async def download_video_and_upload_to_storage(data: VideoSourceData) -> tuple[bytes | None, CloudStorageDataDict | None]:
    """
    Download media (video or slideshow) and upload it to storage

    Args:
        data (VideoSourceData): Dictionary containing media information
            Format: {
                'url': str,  # Video URL if video
                'images': list,  # List of image URLs if slideshow
                'id': str  # Video/Post ID
            }

    Returns:
        tuple[bytes | None, CloudStorageDataDict | None]: Tuple containing the video bytes and storage data
    """
    print("Video data", data)

    media_bytes = await download_tiktok_media(data)
    if not media_bytes:
        return None, None

    storage_data = await upload_media_to_storage(data["id"], media_bytes)
    return media_bytes, storage_data


def save_in_db(data: dict) -> str | None:
    """
    Save media information to the database

    Args:
        data (dict): Dictionary containing media information
    """
    try:
        result = db["tiktoks_aweme"].insert_one(data)
        return result.inserted_id
    except Exception as e:
        logging.error(f"Error saving tiktok data skipping: {e}")
        return None
