import datetime
from typing import Optional
import pydantic
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import SQLModel, Field, Relationship
from . import users

class BaseArticle(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    author: str
    authorProfileImage: str
    title: str
    content: str
    articleImage: str | None = None
    reader: int | None = 0
    dateOfLastRead: datetime.datetime | None = None
    user_id: int 

class Article(BaseArticle):
    id: int
    dateOfPublish: datetime.datetime
    dateOfLastRead: datetime.datetime | None = None

class ReadArticle(BaseModel):
    reader: int 
    dateOfLastRead: datetime.datetime = Field(default_factory=datetime.datetime.now)

class CreateArticle(BaseModel):
    title: str
    content: str
    articleImage: str | None = None


class UpdataPost(BaseArticle):
    pass

class DBArticle(BaseArticle, SQLModel, table=True):
    __tablename__ = "articles"
    id: Optional[int] = Field(default=None, primary_key=True)
    dateOfPublish: datetime.datetime = Field(default_factory=datetime.datetime.now)

    user_id: int = Field(default=None, foreign_key="users.id")
    user: users.DBUser | None = Relationship()


class ArticleList(BaseModel):
    articles: list[Article]
    page: int
    page_size: int
    size_per_page: int