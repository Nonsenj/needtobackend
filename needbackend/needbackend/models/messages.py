# from typing import Optional, List
# from pydantic import BaseModel, ConfigDict
# from sqlmodel import Field, SQLModel, Relationship
# from datetime import datetime
# from . import users, groupchats, individualchats

# # Base model for the message fields
# class BaseMessage(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     content: str
#     timestamp: datetime = Field(default_factory=datetime.utcnow)
#     sender_id: int
#     group_id: Optional[int] = None
#     chat_id: Optional[int] = None

# # Pydantic model for creating a new message
# class CreatedMessage(BaseMessage):
#     pass

# # Pydantic model for updating a message
# class UpdatedMessage(BaseMessage):
#     pass

# # Pydantic model for reading a message
# class Message(BaseMessage):
#     id: int

# # SQLModel for the Message table in the database
# class DBMessage(BaseMessage, SQLModel, table=True):
#     __tablename__ = "messages"
#     id: Optional[int] = Field(default=None, primary_key=True)
    
#     sender_id: int = Field(foreign_key="users.id")
#     sender: Optional[users.DBUser] = Relationship()

#     group_id: Optional[int] = Field(default=None, foreign_key="groupchats.id")
#     group: Optional[groupchats.DBGroupChat] = Relationship()

#     chat_id: Optional[int] = Field(default=None, foreign_key="individualchats.id")
#     chat: Optional[individualchats.DBIndividualChat] = Relationship()

# # Pydantic model for a list of messages (e.g., in a chat or group)
# class MessageList(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     messages: List[Message]
#     page: int
#     page_count: int
#     size_per_page: int
