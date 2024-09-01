import datetime
from typing import Optional
import pydantic
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import SQLModel, Field, Relationship

class BaseBlog(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str = Field(index=True)
    subtitle: str | None = None
    content: str | None = None
    user_id: int
    completed: bool | None = False

# class BaseTag(BaseModel):
#     name: str = Field(index=True)

# class BlogTagLink(SQLModel, table=True):
#     tag_id: int | None = Field(default=None, foreign_key="tags.id", primary_key=True)
#     blog_id: int | None = Field(default=None, foreign_key="blogs.id", primary_key=True)


# class DBTag(BaseTag, SQLModel, table=True):
#     __tablename__ = "tags"
#     id: int | None = Field(default=None, primary_key=True)

#     list_blog: list["DBBlog"] = Relationship(back_populates="list_tag", link_model=BlogTagLink)

class DBBlog(BaseBlog, SQLModel, table=True):
    __tablename__ = "blogs"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    # list_tag: list["DBTag"] = Relationship(back_populates="list_blog", link_model=BlogTagLink, sa_relationship_kwargs={'lazy':'selectin'})

class Blog(BaseBlog):
    id: int
    created_at: datetime.datetime
    # tags: list[DBTag]

class CreateBlog(BaseBlog):
    pass
    # tags: list[DBTag]

class UpdataBlog(BaseBlog):
    pass

class BlogList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    blogs: list[Blog]
    page: int
    page_size: int
    size_per_page: int