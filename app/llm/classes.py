from enum import Enum
from typing import TypedDict


class ChatRole(str, Enum):
    Assistant = "assistant",
    System = "system",
    User = "user",

class ChatMessageDict(TypedDict):
    role: ChatRole
    content: str