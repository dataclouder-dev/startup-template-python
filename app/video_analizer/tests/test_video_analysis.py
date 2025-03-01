import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from app.video_analizer.services import video_analizer_service


def test_get_tiktok_sources() -> None:
    data = video_analizer_service.get_tiktok_sources("7475811608451714359")
    print(data)


async def test_video_analysis() -> None:
    tiktok_url = "https://www.tiktok.com/@polilan_app/video/7475811608451714359"
    print("Downloading tiktok video", tiktok_url)
    await video_analizer_service.download_tiktok_upload_files_and_update_db(tiktok_url)


if __name__ == "__main__":
    # The only way to run and test async functions.
    print("Running simple file")

    result = asyncio.run(test_video_analysis())
    print(result)
