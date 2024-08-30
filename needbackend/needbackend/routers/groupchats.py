# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlmodel.ext.asyncio.session import AsyncSession
# from sqlmodel import select
# from typing import List, Annotated

# from .. import deps
# from ..models import DBGroupChat, GroupChat, CreatedGroupChat, UpdatedGroupChat, GroupChatList, GroupChatMember, get_session, DBUser

# router = APIRouter(prefix="/groupchats", tags=["groupchats"])

# # Create a new group chat
# @router.post("/", response_model=GroupChat)
# async def create_group_chat(
#     group_chat_info: CreatedGroupChat,
#     session: Annotated[AsyncSession, Depends(get_session)],
#     current_user = Depends(deps.get_current_user)
# ) -> GroupChat:

#     group_chat = DBGroupChat(
#         name=group_chat_info.name,
#         description=group_chat_info.description,
#     )
#     session.add(group_chat)
#     await session.commit()
#     await session.refresh(group_chat)

#     # Add the current user as a member of the group chat
#     member = GroupChatMember(
#         user_id=current_user.id,
#         group_chat_id=group_chat.id
#     )
#     session.add(member)
#     await session.commit()

#     return group_chat

# # Get all group chats for the current user
# @router.get("/", response_model=List[GroupChat])
# async def list_group_chats(
#     session: Annotated[AsyncSession, Depends(get_session)],
#     current_user = Depends(deps.get_current_user)
# ) -> List[GroupChat]:

#     query = select(DBGroupChat).join(GroupChatMember).where(GroupChatMember.user_id == current_user.id)
#     result = await session.exec(query)
#     group_chats = result.all()

#     return group_chats

# @router.post("/noauth", response_model=GroupChat)
# async def create_anonymous_group_chat(
#     group_chat_info: CreatedGroupChat,
#     session: Annotated[AsyncSession, Depends(get_session)]
# ) -> GroupChat:

#     group_chat = DBGroupChat(
#         name=group_chat_info.name,
#         description=group_chat_info.description,
#     )
#     session.add(group_chat)
#     await session.commit()
#     await session.refresh(group_chat)

#     # Add a default member to the group chat (e.g. an anonymous user)
#     member = GroupChatMember(
#         user_id=None,  # or some default value
#         group_chat_id=group_chat.id
#     )
#     session.add(member)
#     await session.commit()

#     return group_chat


# # Add a member to a group chat
# @router.post("/{group_chat_id}/members", response_model=GroupChat)
# async def add_member_to_group_chat(
#     group_chat_id: int,
#     user_id: int,
#     session: Annotated[AsyncSession, Depends(get_session)],
#     current_user = Depends(deps.get_current_user)
# ) -> GroupChat:

#     group_chat = await session.get(DBGroupChat, group_chat_id)
#     if not group_chat:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Group chat not found.",
#         )

#     member = GroupChatMember(
#         user_id=user_id,
#         group_chat_id=group_chat.id
#     )
#     session.add(member)
#     await session.commit()

#     return group_chat

# # Update group chat details
# @router.put("/{group_chat_id}", response_model=GroupChat)
# async def update_group_chat(
#     group_chat_id: int,
#     group_chat_update: UpdatedGroupChat,
#     session: Annotated[AsyncSession, Depends(get_session)],
#     current_user = Depends(deps.get_current_user)
# ) -> GroupChat:

#     group_chat = await session.get(DBGroupChat, group_chat_id)
#     if not group_chat:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Group chat not found.",
#         )

#     group_chat.name = group_chat_update.name
#     group_chat.description = group_chat_update.description
#     session.add(group_chat)
#     await session.commit()
#     await session.refresh(group_chat)

#     return group_chat

# # Delete a group chat
# @router.delete("/{group_chat_id}")
# async def delete_group_chat(
#     group_chat_id: int,
#     session: Annotated[AsyncSession, Depends(get_session)],
#     current_user = Depends(deps.get_current_user)
# ) -> dict:

#     group_chat = await session.get(DBGroupChat, group_chat_id)
#     if not group_chat:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Group chat not found.",
#         )

#     await session.delete(group_chat)
#     await session.commit()

#     return {"message": "Group chat deleted successfully"}
