import datetime
from typing import Optional , List
import pydantic
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import SQLModel, Field, Relationship

class BaseIndividualChat(BaseModel):
    user1_id: int | None
    user2_id: int | None

class CreatedIndividualChat(BaseIndividualChat):
    pass

class DeletedIndividualChat(BaseIndividualChat):
    pass

class IndividualChat(BaseIndividualChat):
    id : int

class DBIndividualChat(BaseIndividualChat,SQLModel, table=True):
    __tablename__ = "individual_chats"
    id: Optional[int] = Field(default=None, primary_key=True)
    user1_id: int = Field(foreign_key="users.id")
    user2_id: int = Field(foreign_key="users.id")
    created_at: Optional[str] = None

    user1: Optional["DBUser"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[DBIndividualChat.user1_id]"})
    user2: Optional["DBUser"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[DBIndividualChat.user2_id]"})
    messages: List["DBMessage"] = Relationship(back_populates="chat")

class IndividualChatList(BaseIndividualChat):
    model_config = ConfigDict(from_attributes=True)
    IndividualChat: List[IndividualChat]
    page: int
    page_count: int
    size_per_page: int
