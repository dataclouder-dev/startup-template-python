from pydantic import BaseModel


class VideoAnalysisModel(BaseModel):
    url: str
    website: str = "tiktok"
    options: dict = {}
