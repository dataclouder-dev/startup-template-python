from enum import Enum
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel

from app.storage.storage_models import CloudStorageDataDict


class SourceType(str, Enum):
    UNKNOWN = ""
    DOCUMENT = "document"
    WEBSITE = "website"
    YOUTUBE = "youtube"
    NOTION = "notion"
    TIKTOK = "tiktok"


class ImageSource(BaseModel):
    image: CloudStorageDataDict
    description: str
    title: str


class VideoSource(BaseModel):
    idPlatform: str | None = None
    audio: CloudStorageDataDict | None = None
    video: CloudStorageDataDict | None = None
    frames: list[ImageSource] | None = None
    transcription: dict | None = None
    description: str | None = None


class AgentSource(BaseModel):
    _id: ObjectId | None = None
    id: str | None = None
    name: str = ""
    description: str = ""
    type: SourceType = SourceType.UNKNOWN
    sourceUrl: str = ""
    content: str = ""
    contentEnhancedAI: Optional[str] = None
    image: Optional[ImageSource] = None
    video: Optional[VideoSource] = None
    assets: Optional[dict[str, CloudStorageDataDict]] = None
    status: Optional[str] = None
    statusDescription: Optional[str] = None
    relationId: Optional[str] = None
