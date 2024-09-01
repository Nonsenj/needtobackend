import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport


from typing import Any, Dict, Optional
from pydantic_settings import SettingsConfigDict

from needbackend import models, config, main, security
import pytest
import pytest_asyncio

import pathlib
import datetime
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


SettingsTesting = config.Settings
SettingsTesting.model_config = SettingsConfigDict(
    env_file=".testing.env", validate_assignment=True, extra="allow"
)


@pytest.fixture(name="app", scope="session")
def app_fixture():
    settings = SettingsTesting()
    path = pathlib.Path("test-data")
    if not path.exists():
        path.mkdir()

    app = main.create_app(settings)

    asyncio.run(models.recreate_table())

    yield app


@pytest.fixture(name="client", scope="session")
def client_fixture(app: FastAPI) -> AsyncClient:

    # client = TestClient(app)
    # yield client
    # app.dependency_overrides.clear()
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost")


@pytest_asyncio.fixture(name="session", scope="session")
async def get_session() -> models.AsyncIterator[models.AsyncSession]:
    settings = SettingsTesting()
    models.init_db(settings)

    async_session = models.sessionmaker(
        models.engine, class_=models.AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(name="user1")
async def example_user1(session: models.AsyncSession) -> models.DBUser:
    password = "123456"
    username = "user1"

    query = await session.exec(
        models.select(models.DBUser).where(models.DBUser.username == username).limit(1)
    )
    user = query.one_or_none()
    if user:
        return user

    user = models.DBUser(
        username=username,
        password=password,
        email="test@test.com",
        first_name="Firstname",
        last_name="lastname",
        last_login_date=datetime.datetime.now(tz=datetime.timezone.utc),
    )

    await user.set_password(password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest_asyncio.fixture(name="token_user1")
async def oauth_token_user1(user1: models.DBUser) -> dict:
    settings = SettingsTesting()
    access_token_expires = datetime.timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    user = user1
    return models.Token(
        access_token=security.create_access_token(
            data={"sub": user.id},
            expires_delta=access_token_expires,
        ),
        refresh_token=security.create_refresh_token(
            data={"sub": user.id},
            expires_delta=access_token_expires,
        ),
        token_type="Bearer",
        scope="",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        expires_at=datetime.datetime.now() + access_token_expires,
        issued_at=user.last_login_date,
        user_id=user.id,
    )

@pytest_asyncio.fixture(name="admin1")
async def example_admin1(session: models.AsyncSession) -> models.DBUser:
    password = "123456"
    username = "admin1"

    query = await session.exec(
        models.select(models.DBUser).where(models.DBUser.username == username).limit(1)
    )
    admin = query.one_or_none()
    if admin:
        return admin

    admin = models.DBUser(
        username=username,
        password=password,
        email="admin1@example.com",
        first_name="Admin",
        last_name="User",
        last_login_date=datetime.datetime.now(tz=datetime.timezone.utc),
        role=models.UserRole.admin,
    )

    await admin.set_password(password)
    session.add(admin)
    await session.commit()
    await session.refresh(admin)
    return admin


@pytest_asyncio.fixture(name="token_admin1")
async def oauth_token_admin1(admin1: models.DBUser) -> dict:
    settings = SettingsTesting()
    access_token_expires = datetime.timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    admin = admin1
    return models.Token(
        access_token=security.create_access_token(
            data={"sub": admin.id},
            expires_delta=access_token_expires,
        ),
        refresh_token=security.create_refresh_token(
            data={"sub": admin.id},
            expires_delta=access_token_expires,
        ),
        token_type="Bearer",
        scope="",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        expires_at=datetime.datetime.now() + access_token_expires,
        issued_at=admin.last_login_date,
        user_id=admin.id,
    )

@pytest_asyncio.fixture(name="post_user1")
async def example_post_user1(
    session: models.AsyncSession, user1: models.DBUser
) -> models.DBPost:
    content = "Test content"

    query = await session.exec(
        models.select(models.DBPost)
        .where(models.DBPost.content == content, models.DBPost.user_id == user1.id)
        .limit(1)
    )

    post = query.one_or_none()
    if post:
        return post
    
    post = models.DBPost(
        content=content, user_id=user1.id, completed=True
    )

    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

@pytest_asyncio.fixture(name="blog_user1")
async def example_blog_user1(
    session: models.AsyncSession, user1: models.DBUser
) -> models.DBBlog:
    title = "Test Blog Title"

    query = await session.exec(
        models.select(models.DBBlog)
        .where(models.DBBlog.title == title, models.DBBlog.user_id == user1.id)
        .limit(1)
    )

    blog = query.one_or_none()
    if blog:
        return blog
    
    blog = models.DBBlog(
        title=title, content="Test blog content", user_id=user1.id, completed=True
    )

    session.add(blog)
    await session.commit()
    await session.refresh(blog)
    return blog

@pytest_asyncio.fixture(name="comment_post_user1")
async def example_comment_post_user1(
    session: models.AsyncSession, user1: models.DBUser, post_user1: models.DBPost
) -> models.DBCommentPost:
    content = "Test comment on post"

    query = await session.exec(
        models.select(models.DBCommentPost)
        .where(models.DBCommentPost.content == content, models.DBCommentPost.post_id == post_user1.id)
        .limit(1)
    )

    comment = query.one_or_none()
    if comment:
        return comment

    comment = models.DBCommentPost(
        content=content, user_id=user1.id, post_id=post_user1.id, like=0
    )

    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment
