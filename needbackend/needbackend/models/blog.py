import datetime
from typing import Optional
import pydantic
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import SQLModel, Field, Relationship

class BaseBlog(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    subtitle: str | None = None
    content: str | None = None
    author: str
    completed: bool | None = False

class Blog(BaseBlog):
    id: int
    time_stemp: datetime.datetime

class CreateBaseBlog(BaseBlog):
    pass

class UpdataBaseBlog(BaseBlog):
    pass

class DBBlog(BaseBlog, SQLModel, table=True):
    __tablename__ = "blog"
    id: Optional[int] = Field(default=None, primary_key=True)
    time_stemp: datetime.datetime = Field(default_factory=datetime.datetime.now)


class PostList(BaseModel):
    posts: list[Blog]
    page: int
    page_size: int
    size_per_page: int