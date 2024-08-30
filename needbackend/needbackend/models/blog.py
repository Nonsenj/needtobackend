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

class CreateBlog(BaseBlog):
    pass

class UpdataBlog(BaseBlog):
    pass

class DBBlog(BaseBlog, SQLModel, table=True):
    __tablename__ = "blog"
    id: Optional[int] = Field(default=None, primary_key=True)
    time_stemp: datetime.datetime = Field(default_factory=datetime.datetime.now)


class BlogList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    blogs: list[Blog]
    page: int
    page_size: int
    size_per_page: int