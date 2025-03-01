import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from app.video_analizer.services import video_analizer_service
from tools.tiktok_analizer import tiktok_downloader


async def test_download_video() -> None:
    tiktok_url = "https://www.tiktok.com/@polilan_app/video/7475811608451714359"
    print("Downloading tiktok video", tiktok_url)
    await video_analizer_service.download_tiktok_video(tiktok_url)


async def test_download_tiktok_video() -> None:
    tiktok_data: tiktok_downloader.VideoSourceData = {
        "url": "https://v16m.byteicdn.com/3561a3a91bdf82c4280fbc92d4036efb/67c2775a/video/tos/useast2a/tos-useast2a-pve-0068/oAjBHjnIfI0DoBUaQFJx2fE1FEARFgv7zuYKEQ/?a=0&bti=OHYpOTY0Zik3OjlmOm01MzE6ZDQ0MDo%3D&ch=0&cr=0&dr=0&er=0&lr=all&net=0&cd=0%7C0%7C0%7C0&cv=1&br=1060&bt=530&cs=0&ds=6&ft=E3X_A1_fval.9wn5L4BMg.CbrtRhZcA3VifOqH6KJE&mime_type=video_mp4&qs=0&rc=OzVnZTlkOjZkM2g1aWhlO0BpanQ7a3c5cmtweDMzNzczM0A1NS1iXy4tXl4xYl41XjYtYSNfbC5mMmRjZXNgLS1kMTZzcw%3D%3D&vvpl=1&l=20250228205553EECA2EE0751D076517CF&btag=e00088000&cc=10",
        "id": "7475811608451714359",
        "images": [],
    }
    video_bytes, storage_data = await tiktok_downloader.download_video_and_upload_to_storage(tiktok_data)
    print(storage_data)
    print(video_bytes)


if __name__ == "__main__":
    # The only way to run and test async functions.
    print("Running simple file")

    result = asyncio.run(test_download_video())
    print(result)
