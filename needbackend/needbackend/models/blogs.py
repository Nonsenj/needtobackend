import datetime
from typing import Optional
import pydantic
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import SQLModel, Field, Relationship
from . import users
from .comments import CommentOfBlog


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
    author: str
    authorProfileImage: str
    blogImage: str | None = None
    content: str | None = None
    reader: int | None = 0
    user_id: int | None = 0
    dateOfLastRead: datetime.datetime | None = None

class DBBlog(BaseBlog, SQLModel, table=True):
    __tablename__ = "blogs"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    list_tags: list[DBTag] | None = Relationship(back_populates="list_blogs", link_model=BlogTagLink)
    comments: list[Optional["DBCommentBlog"]] = Relationship(back_populates="blog")  # type: ignore
    user_id: int = Field(default=None, foreign_key="users.id")
    user: users.DBUser | None = Relationship()

class Tag(BaseTag):
    id: int

class CreateTag(BaseTag):
    pass

class Blog(BaseBlog):
    id: int
    created_at: datetime.datetime
    dateOfLastRead: datetime.datetime | None = None

class ReadBlog(BaseModel):
    reader: int 
    dateOfLastRead: datetime.datetime = Field(default_factory=datetime.datetime.now)

class BlogWithComments(Blog):
    comments: list[CommentOfBlog] | None = []

class BlogWithTags(Blog):
    list_tags: list[Tag] | None = []

class BlogWithTagComments(BlogWithComments):
    list_tags: list[Tag] | None = []

class CreateBlog(BaseModel):
    title: str = Field(index=True)
    blogImage: str | None = None
    content: str | None = None
    list_tags: list[CreateTag] | None = []

class UpdataBlog(BaseModel):
    title: str = Field(index=True)
    blogImage: str | None = None
    content: str | None = None
    # list_tags: list[CreateTag] | None = []

class BlogList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    blogs: list[BlogWithTags]
    page: int
    page_size: int
    size_per_page: int