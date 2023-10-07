import typing as t
from pydantic import BaseModel

from datetime import datetime
from enum import StrEnum, auto


class WebAppChatType(StrEnum):
    sender = auto()
    private = auto()
    group = auto()
    supergroup = auto()
    channel = auto()


class WebAppUser(BaseModel):
    id: int
    is_bot: bool | None = None
    first_name: str
    last_name: str
    username: str
    language_code: str
    is_premium: t.Literal[True] | None = None
    added_to_attachment_menu: t.Literal[True] | None = None
    allows_write_to_pm: t.Literal[True] | None = None
    photo_url: str | None


class WebAppChat(BaseModel):
    id: str
    type: WebAppChatType  # Notice that this field can only be either "group", "supergroup" or "channel"
    title: str
    username: str | None = None
    photo_url: str | None = None


class WebAppInitData(BaseModel):
    auth_date: datetime
    hash: str
    query_id: str | None = None
    user: WebAppUser | None = None
    receiver: WebAppUser | None = None
    chat: WebAppChat | None = None
    chat_type: WebAppChatType | None = None
    start_param: str | None = None
    can_send_after: int | None = None
