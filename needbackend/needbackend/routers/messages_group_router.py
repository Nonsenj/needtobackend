from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, func
from typing import List, Annotated

from ..deps import get_current_user
from ..models import DBMessageGroup, MessageGroup, CreatedMessageGroup, MessageGroupList , get_session

router = APIRouter(prefix="/messages_group", tags=["messages_group"])


@router.post("/", response_model=MessageGroup)
async def create_message_group(
    message_group: CreatedMessageGroup,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user=Depends(get_current_user)
) -> MessageGroup:
    
    
    db_message_group = DBMessageGroup.model_validate(message_group)
    db_message_group.sender_id = current_user.id  # Automatically set sender_id to the current user

    
    session.add(db_message_group)
    await session.commit()
    await session.refresh(db_message_group)

    
    return MessageGroup.model_validate(db_message_group)


@router.get("/{message_group_id}", response_model=MessageGroup)
async def get_message_group(
    message_group_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user=Depends(get_current_user)
) -> MessageGroup:
    
    
    db_message_group = await session.get(DBMessageGroup, message_group_id)
    if not db_message_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )

    
    return MessageGroup.model_validate(db_message_group)


@router.get("/", response_model=MessageGroupList)
async def list_message_groups(
    session: Annotated[AsyncSession, Depends(get_session)],
    group_chat_id: int,
    page: int = 1,
    size_per_page: int = 10,
    current_user=Depends(get_current_user)
) -> MessageGroupList:
    
    offset = (page - 1) * size_per_page
    
    
    query = select(DBMessageGroup).where(DBMessageGroup.group_chat_id == group_chat_id).offset(offset).limit(size_per_page)
    result = await session.exec(query)
    messages = result.all()

    
    total_count_query = select([func.count(DBMessageGroup.id)]).where(DBMessageGroup.group_chat_id == group_chat_id)
    total_count_result = await session.exec(total_count_query)
    total_count = total_count_result.scalar_one()

    
    page_count = (total_count // size_per_page) + (1 if total_count % size_per_page > 0 else 0)

    
    return MessageGroupList(
        messages=[MessageGroup.from_orm(msg) for msg in messages],
        page=page,
        page_count=page_count,
        size_per_page=size_per_page
    )
