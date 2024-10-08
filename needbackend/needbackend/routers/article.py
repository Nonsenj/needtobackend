from fastapi import APIRouter, HTTPException, Depends, Query

from typing import Optional, Annotated

from sqlmodel import Field, SQLModel, Session, select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

import math
import datetime
from .. import models
from .. import deps

router = APIRouter(prefix="/articles", tags=["articles"])

SIZE_PER_PAGE = 50

@router.get("")
async def read_articles(
    session: Annotated[AsyncSession, Depends(models.get_session)],
    page: int = 1,
) -> models.ArticleList:
    
    result = await session.exec(
        select(models.DBArticle).offset((page-1) * SIZE_PER_PAGE).limit(SIZE_PER_PAGE)
    )

    articles = result.all()
    page_count = int(
        math.ceil(
            (await session.exec(select(func.count(models.DBArticle.id)))).first()
            / SIZE_PER_PAGE
        )
    )

    return models.ArticleList.model_validate(
        dict(articles=articles, page_size=page_count, page=page, size_per_page=SIZE_PER_PAGE)
    )

@router.get("{article_id}")
async def read_article(
    article_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> models.Article:
    db_article = await session.get(models.DBArticle, article_id)
    update_article = models.ReadArticle(reader= db_article.reader + 1)

    db_article.sqlmodel_update(update_article)
    session.add(db_article)
    await session.commit()
    await session.refresh(db_article)

    if db_article:
        return models.Article.model_validate(db_article)
    
    raise HTTPException(status_code=404, detail="Article not found")

@router.post("")
async def create_article(
    article: models.CreateArticle,
    session: Annotated[AsyncSession, Depends(models.get_session)],
    current_user: models.User = Depends(deps.get_current_user), 
) -> models.Article:
    create_article = models.BaseArticle(
        author=current_user.username, 
        authorProfileImage= current_user.profile_img,
        user_id= current_user.id, 
        articleImage= article.articleImage,
        title= article.title,
        content= article.content,
        dateOfLastRead = None,
        reader= None,
    )

    db_article = models.DBArticle.model_validate(create_article)
    session.add(db_article)
    await session.commit()
    await session.refresh(db_article)
    return models.Article.model_validate(db_article)