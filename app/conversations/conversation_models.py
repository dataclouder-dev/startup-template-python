from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field


class CharacterCardData(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    scenario: Optional[str] = None
    first_mes: Optional[str] = None
    creator_notes: Optional[str] = None
    mes_example: Optional[str] = None
    alternate_greetings: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    system_prompt: Optional[str] = None
    post_history_instructions: Optional[str] = None
    character_version: Optional[str] = None
    # extensions: Optional[Dict[str, Any]] = None
    appearance: Optional[str] = None


class CharacterCardDC(BaseModel):
    spec: str = Field(default="chara_card_v2")
    spec_version: str = Field(default="2_v_dc")
    data: CharacterCardData


class Assets(BaseModel):
    image: Any


class TTS(BaseModel):
    voice: str
    secondaryVoice: str
    speed: str
    speedRate: float


class MetaApp(BaseModel):
    isPublished: bool
    isPublic: Any
    authorId: str
    authorEmail: str
    createdAt: datetime
    updatedAt: datetime
    takenCount: int


class IConversationCard(BaseModel):
    version: str
    _id: str
    id: str
    title: str
    assets: Assets
    characterCard: CharacterCardDC
    textEngine: str  # Assuming TextEngines is a string
    conversationType: str  # Assuming ConversationType is a string
    lang: str
    tts: TTS
    metaApp: MetaApp


class TranslationRequest(BaseModel):
    idCard: str
    currentLang: str
    targetLang: str
