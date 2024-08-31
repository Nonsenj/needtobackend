from sqlmodel import SQLModel, Field, Relationship

class DBConversationParticipant(SQLModel, table=True):
    __tablename__ = 'conversation_participants'
    id: int = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key='conversations.id')
    user_id: int = Field(foreign_key='users.id')
    conversation: 'DBConversation' = Relationship(back_populates='conversation_participants')
    user: 'DBUser' = Relationship(back_populates='conversation_participants')