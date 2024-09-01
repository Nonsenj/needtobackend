from typing import AsyncIterator


from sqlmodel import Field, SQLModel, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker


from . import users
from . import posts
from . import admins
from . import feeds
from . import blog
from . import messages_chat
from . import messages_group
from . import individual_chats
from . import group_chats
from . import comment

from .posts import *
from .users import *
from .admins import *
from .feeds import *
from .blog import *
from .messages_chat import *
from .messages_group import *
from .individual_chats import *
from .group_chats import *
from .comment import *


connect_args = {}

engine = None


def init_db(settings):
    global engine

    engine = create_async_engine(
        settings.SQLDB_URL,
        echo=True,
        future=True,
        connect_args=connect_args,
    )


async def recreate_table():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncIterator[AsyncSession]:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


async def close_session():
    global engine
    if engine is None:
        raise Exception("DatabaseSessionManager is not initialized")
    await engine.dispose()