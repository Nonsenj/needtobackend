from typing import Optional
from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel, Relationship
from . import users

# Base model for the individual chat fields
class BaseIndividualChat(BaseModel):
    model_config = ConfigDict(from_attributes=True)

# Pydantic model for creating a new individual chat
class CreatedIndividualChat(BaseIndividualChat):
    user1_id: int
    user2_id: int

# Pydantic model for updating an individual chat
class UpdatedIndividualChat(BaseIndividualChat):
    pass

# Pydantic model for reading an individual chat
class IndividualChat(BaseIndividualChat):
    id: int
    user1: users.DBUser
    user2: users.DBUser

# SQLModel for the IndividualChat table in the database
class DBIndividualChat(BaseIndividualChat, SQLModel, table=True):
    __tablename__ = "individualchats"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    user1_id: int = Field(foreign_key="users.id")
    user2_id: int = Field(foreign_key="users.id")
    
    user1: Optional[users.DBUser] = Relationship(sa_relationship_kwargs={"foreign_keys": "[DBIndividualChat.user1_id]"})
    user2: Optional[users.DBUser] = Relationship(sa_relationship_kwargs={"foreign_keys": "[DBIndividualChat.user2_id]"})
    
    messages: List[DBMessage] = Relationship(back_populates="chat")

# Pydantic model for a list of individual chats
class IndividualChatList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    individual_chats: list[IndividualChat]
    page: int
    page_count: int
    size_per_page: int
