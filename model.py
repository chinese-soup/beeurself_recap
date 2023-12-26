from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TextEntity:
    type: str
    text: str


@dataclass
class Message:
    id: int
    type: str
    from_nickname: str
    from_id: str
    text: str
    text_entities: List[TextEntity]
    date: Optional[str] = None
    date_unixtime: Optional[str] = None
    edited: Optional[str] = None
    edited_unixtime: Optional[str] = None
    reply_to_message_id: Optional[int] = None
    photo: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    # There's more, but we only care about BeeUrself bot's messages,
    # so let's skip it
