import asyncio
import io

from dataclouder_core.exception import handler_exception
from dataclouder_core.models.models import FiltersConfig
from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing_extensions import Any

from app.generics.services import generic_service
from app.video_analizer.models.model import VideoAnalysisModel
from app.video_analizer.services import video_analizer_service
from tools.youtube import yt_dlp_utils, yt_downloads

# from app.agents.services import sources_service

router = APIRouter(prefix="/api/video-analizer", tags=["Video Analizer"])


@router.get("/")
@handler_exception
async def greet() -> dict:
    return {"hi", "hello"}


@router.get("/video-agent-source")
@handler_exception
async def get_video_agent_source(video_platform_id: str) -> list[dict]:
    result = video_analizer_service.get_tiktok_sources(video_platform_id)
    return result


@router.post("/")
@handler_exception
async def start_analysis(video: VideoAnalysisModel, background_tasks: BackgroundTasks) -> dict:
    print("starting video analisis of", video)
    agent_source = video_analizer_service.save_agent_source()

    # Use asyncio.create_task to run the analysis in the background

    asyncio.create_task(video_analizer_service.analize_video(video.url, agent_source))
    # Return immediately without waiting for the background task
    return agent_source.model_dump()


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


@router.post("/download-youtube-video")
@handler_exception
async def download_youtube_video(video: VideoAnalysisModel) -> StreamingResponse:
    print("starting video analisis of", video, video.options)
    media_type = "video/mp4"
    if video.options.get("audio"):
        media_type = "audio/mpeg"
        video_bytes, info_dict = yt_dlp_utils.download_youtube_audio_to_memory(video.url)
    else:
        video_bytes, info_dict = yt_dlp_utils.download_youtube_video_to_memory(video.url)
    print("aqui termino file name", info_dict)

    return StreamingResponse(
        video_bytes,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{info_dict.get("id", "video")}"', "Content-Length": str(video_bytes.getbuffer().nbytes)},
    )
