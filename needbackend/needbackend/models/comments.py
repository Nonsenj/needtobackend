import datetime
from typing import Optional
import pydantic
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import SQLModel, Field, Relationship

from . import users
from . import posts


class BaseComment(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    content: str

class PostComment(BaseComment):
    post_id: int | None = 0
    like: int | None = 0

class BlogComment(BaseComment):
    blog_id: int

class BlogIDComment(BaseComment):
    id: int
    user_id: int 
    
class DBCommentPost(PostComment, SQLModel, table=True):
    __tablename__ = "commentpost"
    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(default=None, foreign_key="users.id")
    user: users.DBUser | None = Relationship()
    post_id: int = Field(default=None, foreign_key="posts.id")
    post: posts.DBPost | None = Relationship()

class DBCommentBlog(BlogComment, SQLModel, table=True):
    __tablename__ = "commentblog"
    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(default=None, foreign_key="users.id")
    user: users.DBUser | None = Relationship()
    blog_id: int = Field(default=None, foreign_key="blogs.id")
    blog:  Optional["DBBlog"]= Relationship(back_populates="comments")  # type: ignore

class CommentOfPost(PostComment):
    id: int 

class CommentOfBlog(BlogComment):
    id: int 

class CreateCommentPost(PostComment):
    pass

class CreateCommentBlog(BlogComment):
    pass

class UpdateCommentPost(PostComment):
    pass

class UpdateCommentBlog(BaseModel):
    content: str

class CommentList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    comments: list[BlogIDComment]
    page: int
    page_size: int
    size_per_page: int