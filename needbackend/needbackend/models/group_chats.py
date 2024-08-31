import datetime
from typing import Optional , List
import pydantic
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import SQLModel, Field, Relationship

class BaseGroupChat(BaseModel):
    name : str
    description: Optional[str] = None

class CreatedGroupChat(BaseGroupChat):
    pass

class DeletedGroupChat(BaseGroupChat):
    pass

class GroupChat(BaseGroupChat):
    id: int

class DBGroupChat(BaseGroupChat,SQLModel, table=True):
    __tablename__ = "group_chats"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    created_at: Optional[str] = None

    members: List["GroupChatMember"] = Relationship(back_populates="group_chat")
    messages: List["DBMessage"] = Relationship(back_populates="group")

class GroupChatMember(SQLModel, table=True):
    __tablename__ = "group_chat_members"
    user_id: int = Field(foreign_key="users.id", primary_key=True)
    group_chat_id: int = Field(foreign_key="group_chats.id", primary_key=True)
    joined_at: Optional[str] = None

    user: Optional["DBUser"] = Relationship(back_populates="group_chats")
    group_chat: Optional[DBGroupChat] = Relationship(back_populates="members")