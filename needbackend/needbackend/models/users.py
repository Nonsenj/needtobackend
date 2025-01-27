import datetime
from typing import Optional , List
import pydantic
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import SQLModel, Field, Relationship

# from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
import bcrypt


class BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    email: str = pydantic.Field(json_schema_extra=dict(example="admin@email.local"))
    username: str = pydantic.Field(json_schema_extra=dict(example="admin"))
    first_name: str | None = None
    last_name: str | None = None
    profile_img: str | None = None
    cover_img: str | None = None


class User(BaseUser):
    id: int
    last_login_date: datetime.datetime | None = pydantic.Field(
        json_schema_extra=dict(example="2023-01-01T00:00:00.000000"), default=None
    )
    register_date: datetime.datetime | None = pydantic.Field(
        json_schema_extra=dict(example="2023-01-01T00:00:00.000000"), default=None
    )

class ReferenceUser(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    username: str
    first_name: str
    last_name: str


class UserList(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    users: list[User]


class Login(BaseModel):
    email: EmailStr
    password: str


class ChangedPassword(BaseModel):
    current_password: str
    new_password: str


class ResetedPassword(BaseModel):
    email: EmailStr
    citizen_id: str


class RegisteredUser(BaseUser):
    password: str = pydantic.Field(json_schema_extra=dict(example="password"))


class UpdatedUser(BaseModel):
    email: str | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    profile_img: str | None = None
    cover_img: str | None = None

class UpdatedImageProfile(BaseModel):
    profile_img: str

class UpdatedImageCover(BaseModel):
    cover_img: str 

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    expires_at: datetime.datetime
    scope: str
    issued_at: datetime.datetime
    user_id: int


class ChangedPasswordUser(BaseModel):
    current_password: str
    new_password: str


class DBUser(BaseUser, SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)

    password: str

    register_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    last_login_date: datetime.datetime | None = Field(default=None)

    async def has_roles(self, roles):
        for role in roles:
            if role in self.roles:
                return True
        return False
    
    async def get_encrypted_password(self, plain_password):
        return bcrypt.hashpw(
            plain_password.encode("utf-8"), salt=bcrypt.gensalt()
        ).decode("utf-8")

    async def set_password(self, plain_password):
        self.password = await self.get_encrypted_password(plain_password)

    async def verify_password(self, plain_password):
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), self.password.encode("utf-8")
        )

# class UserProfile(BaseUser):
#     education_level: str
#     profile_picture: str
#     bio: str
#     phone_number: str
#     secondary_email: str
#     social_media_links: list[str]
#     interests: list[str]
#     activity_status: str
#     role: str

#     async def update_profile(self, updated_data):
#         for key, value in updated_data.items():
#             if hasattr(self, key):
#                 setattr(self, key, value)

# class CreatedUserProfile(UserProfile):
#     pass

# class UpdateUserProfile(UserProfile):
#     pass

# class DeleteUserProfile(UserProfile):
#     pass

