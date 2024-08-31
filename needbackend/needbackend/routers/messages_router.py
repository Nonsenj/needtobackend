from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List, Annotated

from .. import deps
from ..models import DBMessage, get_session , CreatedMessage , Message

router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/", response_model=DBMessage)
async def create_message(
    message: CreatedMessage,
    session: Annotated[AsyncSession, Depends(get_session)]
) -> Message | None:
    session.add(message)
    await session.commit()
    await session.refresh(message)
    return message

@router.get("/{message_id}", response_model=DBMessage)
async def get_message(
    message_id: int,
    session: Annotated[AsyncSession, Depends(get_session)]
) -> Message:
    message = await session.get(DBMessage, message_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return message

@router.get("/", response_model=List[DBMessage])
async def list_messages(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> List[DBMessage]:
    messages = await session.exec(select(DBMessage))
    return messages.all()

@router.delete("/{message_id}")
async def delete_message(
    message_id: int,
    session: Annotated[AsyncSession, Depends(get_session)]
) -> dict:
    message = await session.get(DBMessage, message_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    
    await session.delete(message)
    await session.commit()
    return {"message": "Message deleted successfully"}
