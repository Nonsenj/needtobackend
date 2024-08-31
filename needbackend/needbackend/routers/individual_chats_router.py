from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List, Annotated

from .. import deps
from ..models import DBIndividualChat, get_session

router = APIRouter(prefix="/individual_chats", tags=["individual_chats"])

@router.post("/", response_model=DBIndividualChat)
async def create_individual_chat(
    chat: DBIndividualChat,
    session: Annotated[AsyncSession, Depends(get_session)]
) -> DBIndividualChat:
    session.add(chat)
    await session.commit()
    await session.refresh(chat)
    return chat

@router.get("/{chat_id}", response_model=DBIndividualChat)
async def get_individual_chat(
    chat_id: int,
    session: Annotated[AsyncSession, Depends(get_session)]
) -> DBIndividualChat:
    chat = await session.get(DBIndividualChat, chat_id)
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Individual chat not found")
    return chat

@router.get("/", response_model=List[DBIndividualChat])
async def list_individual_chats(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> List[DBIndividualChat]:
    chats = await session.exec(select(DBIndividualChat))
    return chats.all()

@router.delete("/{chat_id}")
async def delete_individual_chat(
    chat_id: int,
    session: Annotated[AsyncSession, Depends(get_session)]
) -> dict:
    chat = await session.get(DBIndividualChat, chat_id)
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Individual chat not found")
    
    await session.delete(chat)
    await session.commit()
    return {"message": "Individual chat deleted successfully"}
