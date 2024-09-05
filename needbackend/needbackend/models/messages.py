import datetime
from typing import Optional
import pydantic
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import SQLModel, Field, Relationship

from . import users
from . import group_chats

class BaseMessage(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    content: str 
    sender_id: int | None = 0

class MessageIndiChat(BaseMessage) :
    individual_chat_id: int | None = 0

class CreateMessageIndiChat(MessageIndiChat) :
    pass

class MessageGroupChat(BaseMessage) :
    group_chat_id: int | None = 0

class Message(BaseMessage) :
    id: int
    created_at: datetime.datetime

class DBMessageChat(MessageIndiChat, SQLModel, table=True):
    __tablename__ = "messages_chat"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    sender_id: int = Field(foreign_key="users.id")
    sender: users.DBUser = Relationship()

    individual_chat_id: int = Field(default=None, foreign_key="individual_chats.id")
    chat: Optional["DBIndividualChat"] = Relationship()

# class DBMessageGroup(MessageGroupChat, SQLModel, table=True):
#     __tablename__ = "messages_group"
#     id: Optional[int] = Field(default=None, primary_key=True)
#     created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

#     sender_id: int = Field(foreign_key="users.id")
#     sender: users.DBUser = Relationship()

#     group_chat_id: int = Field(default=None, foreign_key="group_chats.id")
#     group: individual_chats.DBIndividualChat = Relationship()

class MessageList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    messages: list[Message]
    page: int
    page_count: int
    size_per_page: int