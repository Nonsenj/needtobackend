import datetime
from typing import Optional
import pydantic
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import SQLModel, Field, Relationship

class BaseMessage(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    message_text: Optional[str] = None
    conversation_id : int | None
    user_id : int | None

class CreatedMessage(BaseMessage) :
    pass

class DeletedMessage(BaseMessage) :
    pass

class Message(BaseMessage) :
    id: int
    message_timestamp: datetime.datetime | None = pydantic.Field(json_schema_extra=dict(example="2023-01-01T00:00:00.000000"), default=None)

class DBMessage(BaseMessage, SQLModel, table=True) :
    __tablename__ = "messages"
    id: int = Field(default=None,primary_key=True)
    conversation_id: int = Field(default=None, foreign_key="conversations.id")
    conversation: conversations.DBConversation | None = Relationship()
