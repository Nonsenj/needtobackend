import datetime
from typing import Optional
import pydantic
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import SQLModel, Field, Relationship

class BaseRank(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    rank_value: int = Field(max_digits=5)
    

class DBRank(BaseRank, SQLModel, table=True):
    __tablename__ = "Rank"
    id: Optional[int] = Field(default=None, primary_key=True)
    time_stemp: datetime.datetime = Field(default_factory=datetime.datetime.now)