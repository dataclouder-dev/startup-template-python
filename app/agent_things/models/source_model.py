from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.storage.storage_models import CloudStorageDataDict


class SourceType(str, Enum):
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
    id_platform: str
    audio: CloudStorageDataDict
    video: CloudStorageDataDict
    frames: list[ImageSource]
    transcript: str
    description: str


class AgentSource(BaseModel):
    id: str
    name: str = ""
    description: str = ""
    type: SourceType
    source_url: str  # Changed from sourceUrl to follow Python naming conventions
    content: str = ""
    content_enhanced_ai: Optional[str] = None  # Changed from contentEnhancedAI
    image: Optional[ImageSource] = None
    video: Optional[VideoSource] = None
    assets: Optional[dict[str, CloudStorageDataDict]] = None
