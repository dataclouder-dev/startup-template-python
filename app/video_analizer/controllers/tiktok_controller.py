from dataclouder_core.exception import handler_exception
from fastapi import APIRouter

from app.video_analizer.repositories import tiktok_repository
from app.video_analizer.services import tiktok_service

router = APIRouter(prefix="/api/video-analizer/tiktok", tags=["Video Analizer Tiktok"])


@router.get("/availible-users")
@handler_exception
async def get_availible_users() -> list:
    result = tiktok_repository.get_author_post_counts()
    return result


@router.get("/user-data")
@handler_exception
async def get_user_data(user_id: str) -> list[dict]:
    result = tiktok_service.get_data_from_tiktoks(user_id)
    return result
