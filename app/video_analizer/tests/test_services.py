import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from app.video_analizer.services import video_analizer_service
from tools.tiktok_analizer import tiktok_downloader


def test_download_video() -> None:
    video_analizer_service.download_video("https://www.tiktok.com/@testuser/video/1234567890")


async def test_download_tiktok_video() -> None:
    tiktok_data: tiktok_downloader.VideoSourceData = {
        "url": "https://www.tiktok.com/@polilan_app/video/7475811608451714359",
        "id": "7475811608451714359",
        "images": [],
    }
    video_bytes, storage_data = await tiktok_downloader.download_video_and_upload_to_storage(tiktok_data)
    print(storage_data)
    print(video_bytes)


if __name__ == "__main__":
    # Run async function
    print("Running simple file")

    asyncio.run(test_download_tiktok_video())
