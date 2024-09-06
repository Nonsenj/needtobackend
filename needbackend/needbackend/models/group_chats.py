import datetime
from typing import Optional , List
import pydantic
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import SQLModel, Field, Relationship

from . import messages as msg
from . import users

class BaseGroupChat(BaseModel):
    name : str
    description: str | None = None

class CreatedGroupChat(BaseGroupChat):
    pass

class DeletedGroupChat(BaseGroupChat):
    pass

class GroupChat(BaseGroupChat):
    id: int

# class GroupMessages(GroupChat):
#     messages: list[msg.MessageGroupChat] = []

class UserGroup(BaseModel):
    id: int
    username: str

class MessageGroup(BaseModel):
    id: int
    sender_id: int

class GroupMessages(GroupChat):
    messages: list[msg.Message] = []
    member: list[UserGroup] = []

class UserGroupLink(UserGroup, SQLModel, table=True):
    user_id: int | None = Field(default=None, foreign_key="users.id", primary_key=True)
    group_id: int | None = Field(default=None, foreign_key="groups.id", primary_key=True)
    joined_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

class DBGroupChat(BaseGroupChat,SQLModel, table=True):
    __tablename__ = "groups"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    messages: list[msg.DBMessageGroup] = Relationship(back_populates="group", sa_relationship_kwargs={'lazy': 'selectin'})
    member: list[users.DBUser] | None = Relationship(link_model=UserGroupLink, sa_relationship_kwargs={'lazy': 'selectin'})

# class GroupChatMember(SQLModel, table=True):
#     __tablename__ = "group_chat_members"
#     user_id: int = Field(foreign_key="users.id", primary_key=True)
#     group_chat_id: int = Field(foreign_key="group_chats.id", primary_key=True)
#     joined_at: Optional[str] = None


# class GroupChatList(BaseModel):
#     group_chats: List[GroupChat]

# class GroupChatMemberList(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     members: List[GroupChatMember]
#     page: int
#     page_count: int
#     size_per_page: int