from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List, Annotated

from .. import deps
from ..models import DBIndividualChat, IndividualChat, IndividualChatCreate, IndividualChatList, get_session, DBUser

router = APIRouter(prefix="/individualchats", tags=["individualchats"])

# Create a new individual chat
@router.post("/", response_model=IndividualChat)
async def create_individual_chat(
    user2_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user = Depends(deps.get_current_user)
) -> IndividualChat:

    existing_chat_query = select(DBIndividualChat).where(
        ((DBIndividualChat.user1_id == current_user.id) & (DBIndividualChat.user2_id == user2_id)) |
        ((DBIndividualChat.user1_id == user2_id) & (DBIndividualChat.user2_id == current_user.id))
    )
    existing_chat = await session.exec(existing_chat_query)
    if existing_chat.one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Individual chat already exists between these users.",
        )

    individual_chat = DBIndividualChat(
        user1_id=current_user.id,
        user2_id=user2_id
    )
    session.add(individual_chat)
    await session.commit()
    await session.refresh(individual_chat)

    return individual_chat

# Get all individual chats for the current user
@router.get("/", response_model=List[IndividualChat])
async def list_individual_chats(
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user = Depends(deps.get_current_user)
) -> List[IndividualChat]:

    query = select(DBIndividualChat).where(
        (DBIndividualChat.user1_id == current_user.id) |
        (DBIndividualChat.user2_id == current_user.id)
    )
    result = await session.exec(query)
    individual_chats = result.all()

    return individual_chats

# Delete an individual chat
@router.delete("/{chat_id}")
async def delete_individual_chat(
    chat_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user = Depends(deps.get_current_user)
) -> dict:

    individual_chat = await session.get(DBIndividualChat, chat_id)
    if not individual_chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Individual chat not found.",
        )

    if current_user.id not in [individual_chat.user1_id, individual_chat.user2_id]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this chat.",
        )

    await session.delete(individual_chat)
    await session.commit()

    return {"message": "Individual chat deleted successfully"}
