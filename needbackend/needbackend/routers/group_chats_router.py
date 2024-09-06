from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List, Annotated

from .. import deps
from .. import models 
router = APIRouter(prefix="/groups", tags=["groups"])

@router.post("/")
async def create_group_chat(
    group_chat: models.CreatedGroupChat,
    current_user: Annotated[models.users, Depends(deps.get_current_user)],
    session: Annotated[AsyncSession, Depends(models.get_session)]
) -> models.GroupChat | None :
    db_group_chat = models.DBGroupChat.model_validate(group_chat)
    db_group_chat.member.append(current_user)
    session.add(db_group_chat)
    await session.commit()
    await session.refresh(db_group_chat)
    return db_group_chat

@router.get("/{group_id}")
async def get_group_chat(
    group_chat_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)]
) -> models.GroupMessages:
    db_group_chat = await session.get(models.DBGroupChat, group_chat_id)
    if not db_group_chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group chat not found")
    return db_group_chat

@router.post("/join/{group_id}")
async def join_group_chat(
    group_chat_id: int,
    current_user: Annotated[models.User, Depends(deps.get_current_user)],
    session: Annotated[AsyncSession, Depends(models.get_session)]
) -> models.GroupChat | None :
    db_group_chat = await session.get(models.DBGroupChat, group_chat_id)

    if not db_group_chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group chat not found")
    
    if any(member.id == current_user.id for member in db_group_chat.member):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="ํYou is already a member of the group chat")
            
    db_group_chat.member.append(current_user)
    session.add(db_group_chat)
    await session.commit()
    await session.refresh(db_group_chat)
    return db_group_chat


# @router.post("/{group_chat_id}/members/{user_id}")
# async def add_member_to_group_chat(
#     group_chat_id: int,
#     user_id: int,
#     current_user: Annotated[users, Depends(get_current_user)],
#     session: Annotated[AsyncSession, Depends(get_session)]
# ) -> dict:
#     group_chat = await session.get(DBGroupChat, group_chat_id)
#     if not group_chat:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group chat not found")
    
#     member = GroupChatMember(user_id=user_id, group_chat_id=group_chat_id)
#     session.add(member)
#     await session.commit()
#     return {"message": "User added to group chat"}

# @router.get("/", response_model=List[DBGroupChat])
# async def list_group_chats(
#     session: Annotated[AsyncSession, Depends(get_session)]
# ) -> List[DBGroupChat]:
#     group_chats = await session.exec(select(DBGroupChat))
#     return group_chats.all()

# @router.delete("/{group_chat_id}")
# async def delete_group_chat(
#     group_chat_id: int,
#     current_user: Annotated[users, Depends(get_current_user)],
#     session: Annotated[AsyncSession, Depends(get_session)]
# ) -> dict:
#     group_chat = await session.get(DBGroupChat, group_chat_id)
#     if not group_chat:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group chat not found")
    
#     await session.exec(select(DBGroupChatMember).where(DBGroupChatMember.group_chat_id == group_chat_id))
#     await session.delete(group_chat)
#     await session.commit()
#     return {"message": "Group chat deleted successfully"}
