import datetime
from typing import Optional
import pydantic
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import SQLModel, Field, Relationship

class BaseMessageChat(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    content: str 
    sender_id: int | None

class CreatedMessageChat(BaseMessageChat) :
    individual_chat_id: int | None

class MessageChat(BaseMessageChat) :
    id: int
    message_timestamp: datetime.datetime | None = pydantic.Field(json_schema_extra=dict(example="2023-01-01T00:00:00.000000"), default=None)

class DBMessageChat(BaseMessageChat,SQLModel, table=True):
    __tablename__ = "messages"
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)

    sender_id: int = Field(foreign_key="users.id")
    sender: Optional["DBUser"] = Relationship(back_populates="messages")

    individual_chat_id: Optional[int] = Field(default=None, foreign_key="individual_chats.id")
    chat: Optional["DBIndividualChat"] = Relationship(back_populates="messages")

class MessageChatList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    messages: list[MessageChat]
    page: int
    page_count: int
    size_per_page: int