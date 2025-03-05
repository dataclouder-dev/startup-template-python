from bson import ObjectId
from dataclouder_core.models.models import FiltersConfig

from app.modules.mongo.mongo import db
from app.video_generator.models.video_model import VideoModel

col_name = "videos"


def find_videos(id: str) -> dict:
    """Get words"""
    collection = db[col_name]
    result = collection.find_one({"_id": ObjectId(id)})

    return result


def find_filtered_videos(filters: FiltersConfig) -> list:
    """Get words"""
    print(filters)
    collection = db[col_name]
    result = collection.find(filters.model_dump())
    return result


def save_video(video: VideoModel) -> VideoModel:
    """Save video insert if not exists, or update if exists"""
    collection = db[col_name]

    # Convert the model to dict for manipulation
    video_dict = video.model_dump()

    if hasattr(video, "id") and video.id:
        # Update existing document
        query = {"_id": ObjectId(video.id)}
        # Remove id from the update data
        video_dict.pop("id", None)
    else:
        # Create new document
        query = {"_id": ObjectId()}

    result = collection.find_one_and_replace(query, video_dict, upsert=True, return_document=True)
    result["_id"] = str(result["_id"])
    return result


def delete_video(id: str) -> VideoModel:
    """Delete video"""
    collection = db[col_name]
    collection.delete_one({"_id": ObjectId(id)})
    return {"message": "Video deleted"}
