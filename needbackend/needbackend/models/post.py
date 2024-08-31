import datetime
from typing import Optional
import pydantic
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import SQLModel, Field, Relationship

class BasePost(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    content: str | None = None
    author: str
    completed: bool | None = False

    #category: str
    likes: int | None = 0
    #dislikes: int | None = 0

class Post(BasePost):
    id: int
    time_stemp: datetime.datetime

class CreatePost(BasePost):
    pass

class UpdataPost(BasePost):
    pass

class DBPost(BasePost, SQLModel, table=True):
    __tablename__ = "post"
    id: Optional[int] = Field(default=None, primary_key=True)
    time_stemp: datetime.datetime = Field(default_factory=datetime.datetime.now)


class PostList(BaseModel):
    posts: list[Post]
    page: int
    page_size: int
    size_per_page: int