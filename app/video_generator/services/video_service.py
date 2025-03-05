from dataclouder_core.models.models import FiltersConfig

from app.video_generator.models.video_model import VideoModel
from app.video_generator.repositories import video_repository


def save_video(video: VideoModel) -> VideoModel:
    return video_repository.save_video(video)


def find_filtered_videos(filters: FiltersConfig) -> VideoModel:
    return video_repository.find_filtered_videos(filters)


def delete_video(id: str) -> VideoModel:
    return video_repository.delete_video(id)
