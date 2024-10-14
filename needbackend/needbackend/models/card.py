import datetime
from typing import Optional
import pydantic
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import SQLModel, Field, Relationship
from . import users

class BaseCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    question: str
    content: str | None = None
    iamge: str | None = None
    answer: str
    completed: bool | None = False

class Card(BaseCard):
    id: int
    create_at: datetime.datetime 

class DBCard(BaseCard, SQLModel, table=True):
    __tablename__ = "cards"
    id: Optional[int] = Field(default=None, primary_key=True)
    create_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    user_id: int = Field(default=None, foreign_key="users.id")
    user: users.DBUser | None = Relationship()

class CardList(BaseModel):
    posts: list[Card]
    page: int
    page_size: int
    size_per_page: int