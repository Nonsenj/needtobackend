from fastapi import APIRouter, Depends, HTTPException, Request, status, UploadFile
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import Field, SQLModel, Session, select, func

from typing import Annotated , List

import uuid
from ..services import directory
from ..services import path_local
from .. import deps
from .. import models

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def get_me(current_user: models.User = Depends(deps.get_current_user)) -> models.User:
    return current_user


@router.get("/{user_id}")
async def get(
    user_id: str,
    session: Annotated[AsyncSession, Depends(models.get_session)],
    current_user: models.User = Depends(deps.get_current_user),
) -> models.User:

    user = await session.get(models.DBUser, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this user",
        )
    return user


@router.post("/create")
async def create(
    user_info: models.RegisteredUser,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> models.User:

    result = await session.exec(
        select(models.DBUser).where(models.DBUser.username == user_info.username)
    )

    user = result.one_or_none()

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This username is exists.",
        )

    user = models.DBUser.from_orm(user_info)
    await user.set_password(user_info.password)
    session.add(user)
    await session.commit()

    return user


@router.put("/{user_id}/change_password")
async def change_password(
    user_id: str,
    password_update: models.ChangedPassword,
    current_user: models.User = Depends(deps.get_current_user),
):

    result = await session.get(models.DBUser, user_id)

    if user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this user",
        )

    if not user.verify_password(password_update.current_password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    user.set_password(password_update.new_password)
    session.add(user)
    await session.commit()


@router.put("/update")
async def update(
    user_update: models.UpdatedUser,
    session: Annotated[AsyncSession, Depends(models.get_session)],
    current_user: models.User = Depends(deps.get_current_user),
) -> models.User:

    db_user = await session.get(models.DBUser, current_user.id)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this user",
        )
    
    db_user.sqlmodel_update(user_update)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user

@router.put("/profile_img")
async def update_profile_img(
    file: UploadFile,
    session: Annotated[AsyncSession, Depends(models.get_session)],
    current_user: models.User = Depends(deps.get_current_user),
) -> models.User:
    path = await directory.Create_Directory_User(current_user.username)
    random_name = str(uuid.uuid4())
    decodeit = open(f"{path}/{random_name}.jpg", 'wb')
    contents = await file.read()
    decodeit.write(contents)
    img_path = await path_local.Create_Path_Image(current_user.username, random_name,)

    user_update = models.UpdatedImageProfile(profile_img=img_path)

    db_user = await session.get(models.DBUser, current_user.id)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this user",
        )
    
    db_user.sqlmodel_update(user_update)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user

@router.put("/cover_img")
async def update_cover_img(
    file: UploadFile,
    session: Annotated[AsyncSession, Depends(models.get_session)],
    current_user: models.User = Depends(deps.get_current_user),
) -> models.User:
    path = await directory.Create_Directory_User(current_user.username)
    random_name = str(uuid.uuid4())
    decodeit = open(f"{path}/{random_name}.jpg", 'wb')
    contents = await file.read()
    decodeit.write(contents)
    img_path = await path_local.Create_Path_Image(current_user.username, random_name,)

    user_update = models.UpdatedImageCover(cover_img=img_path)

    db_user = await session.get(models.DBUser, current_user.id)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this user",
        )
    
    db_user.sqlmodel_update(user_update)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user

@router.get("/", response_model=List[models.DBUser])
async def list_group_chats(
    session: Annotated[AsyncSession, Depends(models.get_session)]
) -> List[models.DBUser]:
    user_list = await session.exec(select(models.DBUser))
    return user_list.all()
    
