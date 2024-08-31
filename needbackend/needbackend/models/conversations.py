import datetime
from typing import Optional
import pydantic

from pydantic import BaseModel, ConfigDict, Field
from sqlmodel import Field, SQLModel, create_engine, Session, select, Relationship

from . import users
from . import messages

class BaseConversation(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    conversation_id : int | None = 1
    user_id : int | None = 1
    user2_id : int | None = 2

class CreatedConversation(BaseConversation) :
    pass

class DeletedConverastion(BaseConversation) :
    pass 


class Conversation(BaseConversation) :
    id : int

class DBConversation(BaseConversation, SQLModel, Table=True) :
    __tablename__ = "conversations"
    conversation_id : int = Field(primary_key=True)
    user_id : int = Field(foreign_key="users.id")
    user2_id : int = Field(foreign_key="users.id")
    users: users.DBUser | None = Relationship()
    messages: "DBMessage" | None = Relationship()

