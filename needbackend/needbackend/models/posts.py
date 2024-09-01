import datetime
from typing import Optional
import pydantic
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import SQLModel, Field, Relationship
from . import users

class BasePost(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    content: str | None = None
    user_id: int 
    completed: bool | None = False

    #category: str
    likes: int | None = 0
    #dislikes: int | None = 0

class Post(BasePost):
    id: int
    create_at: datetime.datetime

class CreatePost(BasePost):
    pass

class UpdataPost(BasePost):
    pass

class DBPost(BasePost, SQLModel, table=True):
    __tablename__ = "posts"
    id: Optional[int] = Field(default=None, primary_key=True)
    create_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    user_id: int = Field(default=None, foreign_key="users.id")
    user: users.DBUser | None = Relationship()


class PostList(BaseModel):
    posts: list[Post]
    page: int
    page_size: int
    size_per_page: int