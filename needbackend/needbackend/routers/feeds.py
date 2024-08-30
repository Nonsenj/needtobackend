from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, func
from typing import List, Annotated

from .. import deps
from .. import models

router = APIRouter(prefix="/feeds", tags=["feeds"])

@router.post("/noauth", response_model=models.ReadFeed)
async def create_anonymous_feed(
    feed_info: models.CreatedFeed,
    session: Annotated[AsyncSession, Depends(models.get_session)]
) -> models.ReadFeed:

    feed = models.DBFeed(
        category=feed_info.category,
        content_id=feed_info.content_id,
        timestamp=feed_info.timestamp,
        user_id=None  # or some default value
    )

    session.add(feed)
    await session.commit()
    await session.refresh(feed)

    return feed

@router.post("/", response_model=models.ReadFeed)
async def create_feed(
    feed_info: models.CreatedFeed,
    session: Annotated[AsyncSession, Depends(models.get_session)],
    current_user: models.User = Depends(deps.get_current_user)
) -> models.ReadFeed:

    feed = models.DBFeed(
        category=feed_info.category,
        content_id=feed_info.content_id,
        timestamp=feed_info.timestamp,
        user_id=current_user.id
    )

    session.add(feed)
    await session.commit()
    await session.refresh(feed)

    return feed

@router.get("/{feed_id}", response_model=models.ReadFeed)
async def get_feed(
    feed_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)],
    current_user: models.User = Depends(deps.get_current_user)
) -> models.ReadFeed:

    feed = await session.get(models.DBFeed, feed_id)
    if not feed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feed item not found.",
        )

    return feed

@router.put("/{feed_id}", response_model=models.ReadFeed)
async def update_feed(
    feed_id: int,
    feed_update: models.UpdatedFeed,
    session: Annotated[AsyncSession, Depends(models.get_session)],
    current_user: models.User = Depends(deps.get_current_user)
) -> models.ReadFeed:

    feed = await session.get(models.DBFeed, feed_id)
    if not feed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feed item not found.",
        )

    feed.category = feed_update.category
    feed.content_id = feed_update.content_id
    feed.timestamp = feed_update.timestamp
    session.add(feed)
    await session.commit()
    await session.refresh(feed)

    return feed

@router.delete("/{feed_id}")
async def delete_feed(
    feed_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)],
    current_user: models.User = Depends(deps.get_current_user)
) -> dict:

    feed = await session.get(models.DBFeed, feed_id)
    if not feed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feed item not found.",
        )

    await session.delete(feed)
    await session.commit()

    return {"message": "Feed item deleted successfully"}

@router.get("/", response_model=models.FeedList)
async def list_feeds(
    session: Annotated[AsyncSession, Depends(models.get_session)],
    current_user: models.User = Depends(deps.get_current_user),
    page: int = 1,
    size_per_page: int = 10
) -> models.FeedList:

    offset = (page - 1) * size_per_page

    # Query to get the list of feeds for the current user with pagination
    query = select(models.DBFeed).where(models.DBFeed.user_id == current_user.id).offset(offset).limit(size_per_page)
    result = await session.exec(query)
    feeds = result.all()

    # Query to get the total count of feeds for the current user
    total_count_query = select([func.count(models.DBFeed.id)]).where(models.DBFeed.user_id == current_user.id)
    total_count = await session.exec(total_count_query)
    total_count = total_count.scalar_one()

    # Calculate total number of pages
    page_count = (total_count // size_per_page) + (1 if total_count % size_per_page > 0 else 0)

    return models.FeedList(
        feeds=feeds,
        page=page,
        page_count=page_count,
        size_per_page=size_per_page
    )