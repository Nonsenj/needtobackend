from fastapi import APIRouter, HTTPException, Depends, Query

from typing import Optional, Annotated

from sqlmodel import Field, SQLModel, Session, select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

import math

from .. import models
from .. import deps

router = APIRouter(prefix="/comments", tags=["comments"])

# @router.post("/post")
# async def create_comment_post(
#     post: models.CreateCommentPost,
#     current_user: Annotated[models.users, Depends(deps.get_current_user)],
#     session: Annotated[AsyncSession, Depends(models.get_session)],
# ) -> models.CommentOfPost | None:
#     db_comment = models.DBCommentPost.model_validate(post)
#     session.add(db_comment)
#     await session.commit()
#     await session.refresh(db_comment)
#     return  models.CommentOfPost.model_validate(db_comment)

@router.post("/blog")
async def create_comment_blog(
    blog: models.CreateCommentBlog,
    current_user: Annotated[models.User, Depends(deps.get_current_user)],
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> models.CommentOfBlog | None:
    db_comment = models.DBCommentBlog.model_validate(blog)
    db_comment.user_id = current_user.id
    session.add(db_comment)
    await session.commit()
    await session.refresh(db_comment)
    return  models.CommentOfBlog.model_validate(db_comment)

# @router.get("/post/{post_id}")
# async def read_comment_blog(
#     post_id: int,
#     session:  Annotated[AsyncSession, Depends(models.get_session)],                            
# ) -> models.CommentOfPost:
#     db_comment = await session.get(models.DBCommentPost, post_id)
#     if db_comment:
#         return models.CommentOfPost.model_validate(db_comment)
    
#     raise HTTPException(status_code=404, detail="Comment not found")

@router.get("/blog/{blog_id}")
async def read_comment_blog(
    blog_id: int,
    session:  Annotated[AsyncSession, Depends(models.get_session)],                            
) -> models.CommentOfBlog:
    result = await session.exec(select(models.DBCommentBlog).where(models.DBCommentBlog.blog_id == blog_id))
    db_comment = result.first()
    if db_comment:
        return models.CommentOfBlog.model_validate(db_comment)
    
    raise HTTPException(status_code=404, detail="Comment not found")

# @router.put("/post/{post_id}")
# async def update_comment_post(
#     post_id: int,
#     comment: models.UpdateCommentPost,
#     current_user: Annotated[models.users, Depends(deps.get_current_user)],
#     session:  Annotated[AsyncSession, Depends(models.get_session)], 
# ) -> models.CommentOfPost:
#     data = comment.model_dump()
#     db_comment = await session.get(models.DBCommentPost, post_id)
#     db_comment.sqlmodel_update(data)
#     session.add(db_comment)
#     await session.commit()
#     await session.refresh(db_comment)

#     return models.CommentOfPost.model_validate(db_comment)

@router.put("/blog/{blog_id}")
async def update_comment_blog(
    blog_id: int,
    comment: models.UpdateCommentBlog,
    current_user: Annotated[models.users, Depends(deps.get_current_user)],
    session:  Annotated[AsyncSession, Depends(models.get_session)], 
) -> models.CommentOfBlog:
    data = comment.model_dump()
    result = await session.exec(select(models.DBCommentBlog).where(models.DBCommentBlog.blog_id == blog_id))
    db_comment = result.first()
    db_comment.sqlmodel_update(data)
    session.add(db_comment)
    await session.commit()
    await session.refresh(db_comment)

    return models.CommentOfBlog.model_validate(db_comment)

# @router.delete("/post/{post_id}")
# async def delete_comment_post(
#     post_id: int,
#     current_user: Annotated[models.users, Depends(deps.get_current_user)],
#     session:  Annotated[AsyncSession, Depends(models.get_session)], 
# ) -> dict:
#     db_comment = await session.get(models.DBCommentPost, post_id)
#     await session.delete(db_comment)
#     await session.commit()

#     return dict(message="delete success")

@router.delete("/blog/{blog_id}")
async def delete_comment_blog(
    blog_id: int,
    current_user: Annotated[models.users, Depends(deps.get_current_user)],
    session:  Annotated[AsyncSession, Depends(models.get_session)], 
) -> dict:
    result = await session.exec(select(models.DBCommentBlog).where(models.DBCommentBlog.blog_id == blog_id))
    db_comment = result.first()
    await session.delete(db_comment)
    await session.commit()

    return dict(message="delete success")