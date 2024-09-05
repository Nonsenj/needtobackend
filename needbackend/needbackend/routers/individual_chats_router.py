from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List, Annotated

from ..deps import get_current_user
from .. import models

router = APIRouter(prefix="/individual_chats", tags=["individual_chats"])

@router.post("/")
async def create_individual_chat(
    individual_chat: models.CreatedIndividualChat,
    current_user: Annotated[models.users, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> models.IndividualChat | None:
    db_individual_chat = models.DBIndividualChat.model_validate(individual_chat)
    session.add(db_individual_chat)
    await session.commit()
    await session.refresh(db_individual_chat)
    return db_individual_chat

@router.get("/{chat_id}")
async def get_individual_chat(
    chat_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)]
) -> models.ChatMessages:
    chat = await session.get(models.DBIndividualChat, chat_id)
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Individual chat not found")
    return chat

# @router.get("/", response_model=List[DBIndividualChat])
# async def list_individual_chats(
#     session: Annotated[AsyncSession, Depends(get_session)]
# ) -> List[DBIndividualChat]:
#     chats = await session.exec(select(DBIndividualChat))
#     return chats.all()

# @router.delete("/{chat_id}")
# async def delete_individual_chat(
#     chat_id: int,
#     current_user: Annotated[users, Depends(get_current_user)],
#     session: Annotated[AsyncSession, Depends(get_session)]
# ) -> dict:
#     chat = await session.get(DBIndividualChat, chat_id)
#     if not chat:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Individual chat not found")
    
#     await session.delete(chat)
#     await session.commit()
#     return {"message": "Individual chat deleted successfully"}
