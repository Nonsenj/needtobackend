from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List, Annotated

from ..deps import get_current_user 
from ..models import DBMessageChat, MessageChat, CreatedMessageChat, MessageChatList , get_session

router = APIRouter(prefix="/messages_chat", tags=["messages_chat"])


@router.post("/", response_model=MessageChat)
async def create_message_chat(
    message_chat: CreatedMessageChat,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user=Depends(get_current_user)
) -> MessageChat:
    
  
    db_message_chat = DBMessageChat.model_validate(message_chat)
    db_message_chat.sender_id = current_user.id  # Automatically set sender_id to the current user

   
    session.add(db_message_chat)
    await session.commit()
    await session.refresh(db_message_chat)

   
    return MessageChat.model_validate(db_message_chat)


@router.get("/{message_chat_id}", response_model=MessageChat)
async def get_message_chat(
    message_chat_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user=Depends(get_current_user)
) -> MessageChat:
    
    
    db_message_chat = await session.get(DBMessageChat, message_chat_id)
    if not db_message_chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )

    
    return MessageChat.model_validate(db_message_chat)


@router.get("/", response_model=MessageChatList)
async def list_message_chats(
    session: Annotated[AsyncSession, Depends(get_session)],
    individual_chat_id: int,
    page: int = 1,
    size_per_page: int = 10,
    current_user=Depends(get_current_user)
) -> MessageChatList:
    
    offset = (page - 1) * size_per_page
    
    
    query = select(DBMessageChat).where(DBMessageChat.individual_chat_id == individual_chat_id).offset(offset).limit(size_per_page)
    result = await session.exec(query)
    messages = result.all()

   
    total_count_query = select([func.count(DBMessageChat.id)]).where(DBMessageChat.individual_chat_id == individual_chat_id)
    total_count_result = await session.exec(total_count_query)
    total_count = total_count_result.scalar_one()

    
    page_count = (total_count // size_per_page) + (1 if total_count % size_per_page > 0 else 0)


    return MessageChatList(
        messages=[MessageChat.from_orm(msg) for msg in messages],
        page=page,
        page_count=page_count,
        size_per_page=size_per_page
    )
