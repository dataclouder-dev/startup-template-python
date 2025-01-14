from typing import TypedDict, Union, List, Set, Dict, Any, Optional
from enum import Enum
from datetime import datetime

class Message(TypedDict):
    role: str  # Literal['user', 'assistant']
    content: str

class ChatRole(str, Enum):
    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = 'assistant'
    ASSISTANT_HELPER = 'assistantHelper'

class ChatMultiMessage(TypedDict):
    voice: str
    content: str
    text: str
    audioUrl: str
    audioPromise: Any
    isLoading: Optional[bool]
    transcription: Optional[Any]
    transcriptionTimestamps: Optional[List['WordTimestamps']]
    tag: Union[str, List[str], Set[str], Dict[str, Any]]

class TranscriptionsWhisper(TypedDict):
    text: str
    task: str
    language: str
    words: Any
    duration: float

class WordTimestamps(TypedDict):
    word: str
    start: float
    end: float
    highlighted: Any

class ChatMessageDict(TypedDict):
    content: str
    role: ChatRole
    metadata: Optional[Any]

class ChatMessage(TypedDict):
    content: str
    role: ChatRole
    ssml: Optional[str]
    text: Optional[str]
    translation: Optional[str]
    audioUrl: Optional[str]
    audioHtml: Optional[Any]  # HTMLAudioElement equivalent
    promisePlay: Optional[Any]
    stats: Optional[Any]
    multiMessages: Optional[List[ChatMultiMessage]]
    transcription: Optional[TranscriptionsWhisper]
    transcriptionTimestamps: Optional[List[WordTimestamps]]
    voice: Optional[str]

class Appearance(TypedDict):
    physicalDescription: str
    outfit: str
    objects: str
    quirks: str

class CharacterCardDCData(TypedDict):
    name: str
    description: str
    scenario: str
    first_mes: str
    creator_notes: str
    mes_example: str
    alternate_greetings: List[str]
    tags: List[str]
    system_prompt: str
    post_history_instructions: str
    character_version: str
    extensions: Dict[str, Any]
    appearance: Appearance

class CharacterCardDC(TypedDict):
    spec: str  # Literal['chara_card_v2']
    spec_version: str  # Literal['2_v_dc']
    data: CharacterCardDCData

class TextEngines(str, Enum):
    PLANTEXT = 'plantext'
    SIMPLE_TEXT = 'simpleText'
    MARKDOWN_MULTI_MESSAGES = 'markdownMultiMessages'
    MARKDOWN_SSML = 'markdownSSML'

class ConversationType(str, Enum):
    GENERAL = 'general'
    REFLECTION = 'reflection'
    LEARNING_EXAMPLE = 'learningExample'
    CHALLENGE = 'challenge'

class TTSConfig(TypedDict):
    voice: str
    secondaryVoice: str
    speed: str
    speedRate: float

class MetaApp(TypedDict):
    isPublished: bool
    isPublic: Any
    authorId: str
    authorEmail: str
    createdAt: datetime
    updatedAt: datetime
    takenCount: int

class Assets(TypedDict):
    image: Any

class IConversationCard(TypedDict):
    version: str
    id: str
    title: str
    assets: Assets
    characterCard: CharacterCardDC
    textEngine: TextEngines
    conversationType: ConversationType
    lang: str
    tts: TTSConfig
    metaApp: MetaApp


LangCodeDescription = {
    'es': 'Spanish',
    'en': 'English',
    'it': 'Italian',
    'pt': 'Portuguese',
    'fr': 'French',
    }