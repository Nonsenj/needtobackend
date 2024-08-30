from fastapi import APIRouter, HTTPException, Depends, Query

from typing import Optional, Annotated

from sqlmodel import Field, SQLModel, Session, select, func
from sqlmodel.ext.asyncio.session import AsyncSession

import math

from .. import models
from .. import deps

router = APIRouter(prefix="/post", tags=["posts"])

SIZE_PER_PAGE = 50

@router.get("")
async def read_items(
    session: Annotated[AsyncSession, Depends(models.get_session)],
    page: int = 1,
) -> models.PostList:
    
    result = await session.exec(
        select(models.DBPost).offset((page-1) * SIZE_PER_PAGE).limit(SIZE_PER_PAGE)
    )

    posts = result.all()
    page_count = int(
        math.ceil(
            (await session.exec(select(func.count(models.DBPost.id)))).first()
            / SIZE_PER_PAGE
        )
    )

    return models.PostList.model_validate(
        dict(posts=posts, page_count=page_count, page=page, size_per_page=SIZE_PER_PAGE)
    )

@router.post("/noauth")
async def create_anonymous_post(
    post: models.CreatePost,
    session: Annotated[AsyncSession, Depends(models.get_session)]
) -> models.Post | None:
    db_post = models.DBPost.model_validate(post)
    session.add(db_post)
    await session.commit()
    await session.refresh(db_post)
    return models.Post.model_validate(db_post)

@router.post("")
async def create_post(
    post: models.CreatePost,
    current_user: Annotated[models.users, Depends(deps.get_current_user)],
    session: Annotated[AsyncSession, Depends(models.get_session)]
) -> models.Post | None:
    db_post = models.DBPost.model_validate(post)
    session.add(db_post)
    await session.commit()
    await session.refresh(db_post)
    return  models.Post.model_validate(db_post)

@router.get("/{post_id}")
async def read_post(
    post_id: int,
    session:  Annotated[AsyncSession, Depends(models.get_session)],                            
) -> models.Post:
    db_post = await session.get(models.DBPost, post_id)
    print(db_post)
    if db_post:
        return models.Post.model_validate(db_post)
    
    raise HTTPException(status_code=404, detail="Post not found")

@router.put("/{post_id}")
async def update_post(
    post_id: int,
    post: models.UpdataPost,
    current_user: Annotated[models.users, Depends(deps.get_current_user)],
    session:  Annotated[AsyncSession, Depends(models.get_session)], 
) -> models.Post:
    data = post.model_dump()
    db_post = await session.get(models.DBPost, post_id)
    session.add(db_post)
    await session.commit()
    await session.refresh(db_post)

    return models.Post.model_validate(db_post)

@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    current_user: Annotated[models.users, Depends(deps.get_current_user)],
    session:  Annotated[AsyncSession, Depends(models.get_session)], 
) -> dict:
    db_post = await session.get(models.DBPost, post_id)
    await session.delete(db_post)
    await session.commit()

    return dict(message="delete success")
    