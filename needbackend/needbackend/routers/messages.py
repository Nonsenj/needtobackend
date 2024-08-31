from fastapi import APIRouter, HTTPException, Path, Query
from sqlmodel import Session, select
from typing import List

from .models import DBMessage, Message

router = APIRouter(prefix="/messages", tags=["messages"])

@router.get("", response_model=List[Message])
async def read_messages(conversation_id: int = Query(None, description="Filter by conversation ID")):
    with Session(engine) as session:
        if conversation_id:
            messages = session.exec(select(DBMessage).where(DBMessage.conversation_id == conversation_id)).all()
        else:
            messages = session.exec(select(DBMessage)).all()
        return [Message.from_orm(message) for message in messages]

@router.get("/{message_id}", response_model=Message)
async def read_message(message_id: int = Path(..., description="Message ID")):
    with Session(engine) as session:
        message = session.get(DBMessage, message_id)
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        return Message.from_orm(message)

@router.post("", response_model=Message)
async def create_message(message: CreatedMessage):
    with Session(engine) as session:
        db_message = DBMessage.from_orm(message)
        session.add(db_message)
        session.commit()
        session.refresh(db_message)
        return Message.from_orm(db_message)

@router.delete("/{message_id}")
async def delete_message(message_id: int = Path(..., description="Message ID")):
    with Session(engine) as session:
        message = session.get(DBMessage, message_id)
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        session.delete(message)
        session.commit()
        return {"message": "Message deleted"}