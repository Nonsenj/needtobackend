from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel, Relationship
from . import users

# Base model for the group chat fields
class BaseGroupChat(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: Optional[str] = None

# Pydantic model for creating a new group chat
class CreatedGroupChat(BaseGroupChat):
    pass

# Pydantic model for updating a group chat
class UpdatedGroupChat(BaseGroupChat):
    pass

# Pydantic model for reading a group chat
class GroupChat(BaseGroupChat):
    id: int
    members: List[users.DBUser] = []

# SQLModel for the GroupChat table in the database
class DBGroupChat(BaseGroupChat, SQLModel, table=True):
    __tablename__ = "groupchats"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    name: str = Field(...)
    description: Optional[str] = Field(default=None)
    
    members: List[GroupChatMember] = Relationship(back_populates="group_chat")
    messages: List[DBMessage] = Relationship(back_populates="group")

# SQLModel for the GroupChatMember table to handle many-to-many relationships between GroupChats and Users
class GroupChatMember(SQLModel, table=True):
    __tablename__ = "groupchat_members"
    user_id: int = Field(foreign_key="users.id", primary_key=True)
    group_chat_id: int = Field(foreign_key="groupchats.id", primary_key=True)
    
    user: Optional[users.DBUser] = Relationship(back_populates="group_chats")
    group_chat: Optional[DBGroupChat] = Relationship(back_populates="members")

# Pydantic model for a list of group chats
class GroupChatList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    group_chats: List[GroupChat]
    page: int
    page_count: int
    size_per_page: int
