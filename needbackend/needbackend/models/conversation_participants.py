from sqlmodel import SQLModel, Field, Relationship

from . import users
from . import messag

class BaseConversation_participant(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    conversation_id : int | None = 1
    user_id : int | None = 1

class CreatedTransaction(BaseTransaction):
    pass


class Conversation_participants(BaseConversation_participant) :
    id : int
    conversation_id : int
    user_id : int

class DBConversationParticipant(BaseConversation_participant ,SQLModel, table=True):
    __tablename__ = 'conversation_participants'
    id: int = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key='conversations.id')
    user_id: int = Field(foreign_key='users.id')
    conversation: 'DBConversation' = Relationship(back_populates='conversation_participants')
    user: 'DBUser' = Relationship(back_populates='conversation_participants')

class Conversation_participantsList(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    conversation_participants : list[Conversation_participants]
    Page: int
    page_count: int
    size_per_page: int