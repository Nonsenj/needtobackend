from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List, Annotated

from .. import deps
from ..models import DBMessageChat, get_session , CreatedMessageChat , MessageChat , CreatedMessageGroup , DBMessageGroup , MessageGroup

router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/group_message", response_model=DBMessageGroup)
async def create_message_group_chat(
    message: CreatedMessageGroup,
    session: Annotated[AsyncSession, Depends(get_session)]
) -> MessageGroup | None:
    db_message = DBMessage(**message.dict())
    session.add(db_message)
    await session.commit()
    await session.refresh(db_message)
    return DBMessage.model_validate(db_message)

@router.post("/individual_message", response_model=DBMessageChat)
async def create_message_individual_chat(
    message: CreatedMessageChat,
    session: Annotated[AsyncSession, Depends(get_session)]
) -> MessageChat | None:
    db_message = DBMessage(**message.dict())
    session.add(db_message)
    await session.commit()
    await session.refresh(db_message)
    return DBMessage.model_validate(db_message)

@router.get("/individual_message/{message_id}", response_model=DBMessageChat)
async def get_message_chat(
    message_id: int,
    session: Annotated[AsyncSession, Depends(get_session)]
) -> MessageChat:
    message = await session.get(DBMessageChat, message_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return message

@router.get("/group_message/{message_id}", response_model=DBMessageGroup)
async def get_message_group(
    message_id: int,
    session: Annotated[AsyncSession, Depends(get_session)]
) -> MessageGroup:
    message = await session.get(DBMessageGroup, message_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return message

@router.get("/individual_message_list", response_model=List[DBMessageChat])
async def list_messages_group(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> List[DBMessageChat]:
    messages = await session.exec(select(DBMessageChat))
    return messages.all()


@router.get("/group_message_list", response_model=List[DBMessageGroup])
async def list_messages_group(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> List[DBMessageGroup]:
    messages = await session.exec(select(DBMessageGroup))
    return messages.all()



@router.delete("/individual_message/{message_id}")
async def delete_message_chat(
    message_id: int,
    session: Annotated[AsyncSession, Depends(get_session)]
) -> dict:
    message = await session.get(DBMessageChat, message_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    
    await session.delete(message)
    await session.commit()
    return {"message": "Message deleted successfully"}

@router.delete("/group_message/{message_id}")
async def delete_message_chat(
    message_id: int,
    session: Annotated[AsyncSession, Depends(get_session)]
) -> dict:
    message = await session.get(DBMessageGroup, message_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    
    await session.delete(message)
    await session.commit()
    return {"message": "Message deleted successfully"}