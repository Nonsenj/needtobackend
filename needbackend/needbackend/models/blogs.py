import datetime
from typing import Optional
import pydantic
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import SQLModel, Field, Relationship

class BlogTagLink(SQLModel, table=True):
    blog_id: int | None = Field(default=None, foreign_key="blogs.id", primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="tags.id", primary_key=True)

class BaseTag(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str 

class DBTag(BaseTag, SQLModel, table=True):
    __tablename__ = "tags"
    id: Optional[int] = Field(default=None, primary_key=True)

    list_blogs: list["DBBlog"] = Relationship(back_populates="list_tags", link_model=BlogTagLink)

class BaseBlog(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str = Field(index=True)
    subtitle: str | None = None
    content: str | None = None
    user_id: int | None = 0
    completed: bool | None = False

class DBBlog(BaseBlog, SQLModel, table=True):
    __tablename__ = "blogs"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    list_tags: list[DBTag] | None = Relationship(back_populates="list_blogs", link_model=BlogTagLink)

class Tag(BaseTag):
    id: int

class CreateTag(BaseTag):
    pass

class Blog(BaseBlog):
    id: int
    created_at: datetime.datetime

class BlogWithTag(BaseBlog):
    id: int
    created_at: datetime.datetime
    list_tags: list[Tag] | None = []


class CreateBlog(BaseBlog):
    list_tags: list[CreateTag] | None = []

class UpdataBlog(BaseBlog):
    pass

class BlogList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    blogs: list[BlogWithTag]
    page: int
    page_size: int
    size_per_page: int