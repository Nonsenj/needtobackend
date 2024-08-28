from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List, Annotated

from .. import deps
from ..models import DBMessage, Message, MessageCreate, DBGroupChat, DBIndividualChat, get_session

router = APIRouter(prefix="/messages", tags=["messages"])

# Get messages for a group chat
@router.get("/group/{group_id}", response_model=List[Message])
async def get_group_messages(
    group_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user = Depends(deps.get_current_user)
) -> List[Message]:

    query = select(DBMessage).where(DBMessage.group_id == group_id)
    result = await session.exec(query)
    messages = result.all()

    if not messages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No messages found for this group chat.",
        )

    return messages

# Get messages for an individual chat
@router.get("/chat/{chat_id}", response_model=List[Message])
async def get_individual_messages(
    chat_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user = Depends(deps.get_current_user)
) -> List[Message]:

    query = select(DBMessage).where(DBMessage.chat_id == chat_id)
    result = await session.exec(query)
    messages = result.all()

    if not messages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No messages found for this individual chat.",
        )

    return messages

# Create a new message in a group chat
@router.post("/group/{group_id}", response_model=Message)
async def create_group_message(
    group_id: int,
    message_info: MessageCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user = Depends(deps.get_current_user)
) -> Message:

    group_chat = await session.get(DBGroupChat, group_id)
    if not group_chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group chat not found.",
        )

    message = DBMessage(
        content=message_info.content,
        sender_id=current_user.id,
        group_id=group_id,
        timestamp=message_info.timestamp
    )

    session.add(message)
    await session.commit()
    await session.refresh(message)

    return message

# Create a new message in an individual chat
@router.post("/chat/{chat_id}", response_model=Message)
async def create_individual_message(
    chat_id: int,
    message_info: MessageCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user = Depends(deps.get_current_user)
) -> Message:

    individual_chat = await session.get(DBIndividualChat, chat_id)
    if not individual_chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Individual chat not found.",
        )

    message = DBMessage(
        content=message_info.content,
        sender_id=current_user.id,
        chat_id=chat_id,
        timestamp=message_info.timestamp
    )

    session.add(message)
    await session.commit()
    await session.refresh(message)

    return message

# Delete a message
@router.delete("/{message_id}")
async def delete_message(
    message_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user = Depends(deps.get_current_user)
) -> dict:

    message = await session.get(DBMessage, message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found.",
        )

    if message.sender_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this message.",
        )

    await session.delete(message)
    await session.commit()

    return {"message": "Message deleted successfully"}
