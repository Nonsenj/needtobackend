import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import SQLModel, Field
import pydantic
class BaseAdmin(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    email: str = pydantic.Field(json_schema_extra=dict(example="admin@email.local"))
    username: str = pydantic.Field(json_schema_extra=dict(example="admin"))
    first_name: str = pydantic.Field(json_schema_extra=dict(example="Firstname"))
    last_name: str = pydantic.Field(json_schema_extra=dict(example="Lastname"))


class Admin(BaseAdmin):
    id: int
    last_login_date: datetime.datetime | None = pydantic.Field(
        json_schema_extra=dict(example="2023-01-01T00:00:00.000000"), default=None
    )
    register_date: datetime.datetime | None = pydantic.Field(
        json_schema_extra=dict(example="2023-01-01T00:00:00.000000"), default=None
    )


class DBAdmin(BaseAdmin, SQLModel, table=True):
    __tablename__ = "admins"
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


class AdminLogin(BaseModel):
    email: EmailStr
    password: str


class AdminChangedPassword(BaseModel):
    current_password: str
    new_password: str


class AdminResetedPassword(BaseModel):
    email: EmailStr
    citizen_id: str


class AdminToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    expires_at: datetime.datetime
    scope: str
    issued_at: datetime.datetime
    admin_id: int