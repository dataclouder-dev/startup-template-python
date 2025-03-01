import io

from dataclouder_core.exception import handler_exception
from dataclouder_core.models.models import FiltersConfig
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from typing_extensions import Any

from app.generics.services import generic_service
from app.video_analizer.models.model import VideoAnalysisModel
from app.video_analizer.services import video_analizer_service
from tools.youtube import yt_downloads

# from app.agents.services import sources_service

router = APIRouter(prefix="/api/video-analizer", tags=["Video Analizer"])


@router.get("/")
@handler_exception
async def greet() -> dict:
    return {"hi", "hello"}


# TODO: finish source service
@router.get("/video-agent-source")
@handler_exception
async def get_video_agent_source(video_id: str) -> dict:
    return {"hi", "hello"}


@router.post("/")
@handler_exception
async def start_analysis(video: VideoAnalysisModel) -> dict:
    print("starting video analisis of", video)
    result = await video_analizer_service.analize_video(video.url)
    print(result)

    return {"message": "Analysis started"}


@router.post("/extract-tiktok-data")
@handler_exception
async def save_tiktok_data(video: dict) -> dict:
    print("starting video analisis of", video)
    result = await video_analizer_service.save_tiktok_data(video["urls"])
    print(result)

    return {"message": "Analysis started"}


@router.post("/query")
@handler_exception
async def find_filtered_generics(filters: FiltersConfig) -> list[Any]:
    print(filters)
    generic = generic_service.find_filtered_generics(filters)
    return generic


@router.post("/download-audio")
@handler_exception
async def download_audio(video: VideoAnalysisModel) -> StreamingResponse:
    print("starting video analisis of", video)
    byte, filename, info = await yt_downloads.download_youtube_audio_to_memory(video.url)

    # Convert bytes to BytesIO object
    audio_stream = io.BytesIO(byte)

    # Create response with the audio file
    return StreamingResponse(
        audio_stream,
        media_type="audio/mpeg",  # Adjust content type based on your audio format
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
