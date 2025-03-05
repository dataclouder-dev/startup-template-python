from dataclouder_core.exception import handler_exception
from dataclouder_core.models.models import FiltersConfig
from fastapi import APIRouter

from app.video_generator.models.video_model import VideoModel
from app.video_generator.services import video_service

router = APIRouter(prefix="/api/videos", tags=["Video Generator"])


@router.get("/")
@handler_exception
async def get_video() -> dict:
    return {"hi", "hello"}


@router.get("/{id}")
@handler_exception
async def get_video_by_id(id: str) -> dict:
    return {"id": id}


@router.post("/")
@handler_exception
async def save_video(video: VideoModel) -> VideoModel:
    video = video_service.save_video(video)
    return video


@router.post("/query")
@handler_exception
async def find_filtered_videos(filters: FiltersConfig) -> list:
    print(filters)
    video = video_service.find_filtered_videos(filters)
    return video
