import datetime
from typing import Optional
import pydantic
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import SQLModel, Field, Relationship


class BaseComment(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int | None = 0
    content: str

class PostComment(BaseComment):
    post_id: int | None = 0
    like: int | None = 0

class BlogComment(BaseComment):
    blog_id: int | None = 0

class DBCommentPost(PostComment, SQLModel, table=True):
    __tablename__ = "commentpost"
    id: int | None = Field(default=None, primary_key=True)

    user_id = int = Field(default=None, foreign_key="users.id")
    post_id = int = Field(default=None, foreign_key="posts.id")

class DBCommentBlog(BlogComment, SQLModel, table=True):
    __tablename__ = "commentblog"
    id: int | None = Field(default=None, primary_key=True)

    user_id = int = Field(default=None, foreign_key="users.id")
    blog_id = int = Field(default=None, foreign_key="blogs.id")
