from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from . import users

# Base model for the feed fields
class BaseFeed(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    category: str  # Type of content (e.g., "post", "blog", "rating")
    content_id: int  # ID of the specific content (e.g., Post ID, Blog ID)
    timestamp: datetime = Field(default_factory=datetime.utcnow)  # When the content was added to the feed

# Pydantic model for creating a new feed item
class CreatedFeed(BaseFeed):
    pass

# Pydantic model for updating a feed item
class UpdatedFeed(BaseFeed):
    pass

# Pydantic model for reading a feed item
class ReadFeed(BaseFeed):
    id: int  # Unique identifier for each feed item

# SQLModel for the Feed table in the database
class DBFeed(BaseFeed, SQLModel, table=True):
    __tablename__ = "feeds"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    user_id: int = Field(foreign_key="users.id") 
    user: Optional[users.DBUser] | None = Relationship()  # Relationship to the user who created the feed item

# Pydantic model for a list of feed items (for pagination)
class FeedList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    feeds: List[ReadFeed]
    page: int
    page_count: int
    size_per_page: int
