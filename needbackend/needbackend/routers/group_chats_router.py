from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List, Annotated

from ..deps import get_current_user
from ..models import DBGroupChat, GroupChatMember, get_session, CreatedGroupChat , GroupChat , users

router = APIRouter(prefix="/group_chats", tags=["group_chats"])

@router.post("/", response_model=DBGroupChat)
async def create_group_chat(
    group_chat: CreatedGroupChat,
    current_user: Annotated[users, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
) -> GroupChat | None :
    db_group_chat = DBGroupChat(**group_chat.dict())
    session.add(db_group_chat)
    await session.commit()
    await session.refresh(db_group_chat)
    return db_group_chat

@router.get("/{group_chat_id}", response_model=DBGroupChat)
async def get_group_chat(
    group_chat_id: int,
    session: Annotated[AsyncSession, Depends(get_session)]
) -> GroupChat:
    group_chat = await session.get(DBGroupChat, group_chat_id)
    if not group_chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group chat not found")
    return group_chat

@router.post("/{group_chat_id}/members/{user_id}")
async def add_member_to_group_chat(
    group_chat_id: int,
    user_id: int,
    current_user: Annotated[users, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
) -> dict:
    group_chat = await session.get(DBGroupChat, group_chat_id)
    if not group_chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group chat not found")
    
    member = GroupChatMember(user_id=user_id, group_chat_id=group_chat_id)
    session.add(member)
    await session.commit()
    return {"message": "User added to group chat"}

@router.get("/", response_model=List[DBGroupChat])
async def list_group_chats(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> List[DBGroupChat]:
    group_chats = await session.exec(select(DBGroupChat))
    return group_chats.all()

@router.delete("/{group_chat_id}")
async def delete_group_chat(
    group_chat_id: int,
    current_user: Annotated[users, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
) -> dict:
    group_chat = await session.get(DBGroupChat, group_chat_id)
    if not group_chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group chat not found")
    
    await session.exec(select(DBGroupChatMember).where(DBGroupChatMember.group_chat_id == group_chat_id))
    await session.delete(group_chat)
    await session.commit()
    return {"message": "Group chat deleted successfully"}
