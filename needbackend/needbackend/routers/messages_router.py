from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List, Annotated

from .. import deps
from .. import models

router = APIRouter(prefix="/messages", tags=["messages"])

# @router.post("/group_message", response_model=DBMessage)
# async def create_message_group_chat(
#     message: CreatedMessageGroupChat,
#     session: Annotated[AsyncSession, Depends(get_session)]
# ) -> Message | None:
#     db_message = DBMessage(**message.dict())
#     session.add(db_message)
#     await session.commit()
#     await session.refresh(db_message)
#     return DBMessage.model_validate(db_message)

@router.post("/chat")
async def create_message_individual_chat(
    message: models.CreateMessageIndiChat,
    session: Annotated[AsyncSession, Depends(models.get_session)]
) -> models.Message | None:
    db_message = models.DBMessageChat.model_validate(message)
    session.add(db_message)
    print(db_message)
    await session.commit()
    await session.refresh(db_message)
    return db_message

@router.post("/group")
async def create_message_group_chat(
    message: models.CreateMessageGroupChat,
    session: Annotated[AsyncSession, Depends(models.get_session)]
) -> models.Message | None:
    db_message = models.DBMessageGroup.model_validate(message)
    session.add(db_message)
    print(db_message)
    await session.commit()
    await session.refresh(db_message)
    return db_message

# @router.get("/{message_id}", response_model=DBMessage)
# async def get_message(
#     message_id: int,
#     session: Annotated[AsyncSession, Depends(get_session)]
# ) -> Message:
#     message = await session.get(DBMessage, message_id)
#     if not message:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
#     return message

# @router.get("/", response_model=List[DBMessage])
# async def list_messages(
#     session: Annotated[AsyncSession, Depends(get_session)]
# ) -> List[DBMessage]:
#     messages = await session.exec(select(DBMessage))
#     return messages.all()

# @router.delete("/{message_id}")
# async def delete_message(
#     message_id: int,
#     session: Annotated[AsyncSession, Depends(get_session)]
# ) -> dict:
#     message = await session.get(DBMessage, message_id)
#     if not message:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    
#     await session.delete(message)
#     await session.commit()
#     return {"message": "Message deleted successfully"}
