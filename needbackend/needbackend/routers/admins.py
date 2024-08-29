from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from typing import Annotated

from .. import deps
from .. import models

router = APIRouter(prefix="/admins", tags=["admins"])


@router.get("/me")
def get_me(current_admin: models.User = Depends(deps.get_current_admin)) -> models.User:
    return current_admin


@router.get("/{admin_id}")
async def get(
    admin_id: str,
    session: Annotated[AsyncSession, Depends(models.get_session)],
    current_admin: models.User = Depends(deps.get_current_admin),
) -> models.User:

    admin = await session.get(models.DBUser, admin_id)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this admin",
        )
    return admin


@router.post("/create")
async def create(
    admin_info: models.RegisteredUser,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> models.User:

    result = await session.exec(
        select(models.DBUser).where(models.DBUser.username == admin_info.username)
    )

    admin = result.one_or_none()

    if admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This username is exists.",
        )

    admin = models.DBUser.from_orm(admin_info)
    admin.role = UserRole.admin
    await admin.set_password(admin_info.password)
    session.add(admin)
    await session.commit()

    return admin


@router.put("/{admin_id}/change_password")
async def change_password(
    admin_id: str,
    password_update: models.ChangedPassword,
    current_admin: models.User = Depends(deps.get_current_admin),
) -> dict():

    admin = await session.get(models.DBUser, admin_id)

    if not admin:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this admin",
        )

    if not admin.verify_password(password_update.current_password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    admin.set_password(password_update.new_password)
    session.add(admin)
    await session.commit()


@router.put("/{admin_id}/update")
async def update(
    request: Request,
    admin_id: str,
    admin_update: models.UpdatedUser,
    current_admin: models.User = Depends(deps.get_current_admin),
) -> models.User:

    db_admin = await session.get(models.DBUser, admin_id)

    if not db_admin:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this admin",
        )

    if not db_admin.verify_password(password_update.current_password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    db_admin.sqlmodel_update(admin_update)
    session.add(db_admin)
    await session.commit()
    await session.refresh(db_admin)

    return db_admin