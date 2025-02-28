from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel


class SourceType(str, Enum):
    DOCUMENT = "document"
    WEBSITE = "website"
    YOUTUBE = "youtube"
    NOTION = "notion"
    TIKTOK = "tiktok"


class AgentSource(BaseModel):
    id: str
    name: str = ""
    description: str = ""
    type: SourceType
    source_url: str  # Changed from sourceUrl to follow Python naming conventions
    content: str = ""
    content_enhanced_ai: Optional[str] = None  # Changed from contentEnhancedAI
    img: str = ""
    assets: Optional[Any] = None
