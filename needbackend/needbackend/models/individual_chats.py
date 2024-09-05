import datetime
from typing import Optional
import pydantic
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import SQLModel, Field, Relationship

from . import users
from . import messages as msg

class BaseIndividualChat(BaseModel):
    user1_id: int | None = 0
    user2_id: int | None = 0

class CreatedIndividualChat(BaseIndividualChat):
    pass

class DeletedIndividualChat(BaseIndividualChat):
    pass

class IndividualChat(BaseIndividualChat):
    id: int
    created_at: datetime.datetime

class ChatMessages(IndividualChat):
    messages: list[msg.MessageIndiChat] = []

class DBIndividualChat(BaseIndividualChat,SQLModel, table=True):
    __tablename__ = "individual_chats"
    id: Optional[int] = Field(default=None, primary_key=True)
    user1_id: int = Field(foreign_key="users.id")
    user2_id: int = Field(foreign_key="users.id")

    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    messages: list[msg.DBMessageChat] = Relationship(back_populates="chat", sa_relationship_kwargs={'lazy': 'selectin'})

class IndividualChatList(BaseIndividualChat):
    model_config = ConfigDict(from_attributes=True)
    IndividualChat: list[IndividualChat]
    page: int
    page_count: int
    size_per_page: int
