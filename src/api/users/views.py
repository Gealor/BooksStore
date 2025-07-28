from typing import Annotated, Optional, Sequence
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.auth.tools.tools_auth import get_current_active_auth_user
from core.models import db_helper
from core.schemas.borrowed_books import BorrowedBookInfo, BorrowedBookWithDate
from core.schemas.users import UserBase, UserDelete, UserRead, UserUpdate
from core.config import settings
from core.models.exceptions.book import ListBooksNotFoundException
from core.models.exceptions.user import (
    ListUsersNotFoundException,
    SelfDeleteException,
    UserNotFoundException,
)
from services.user_service import UserService


router = APIRouter(prefix=settings.api.users.prefix, tags=["Users"])


@router.get("/me")
def auth_user_check_self_info(
    user: UserRead = Depends(get_current_active_auth_user),
) -> UserBase:
    return {
        "name": user.name,
        "email": user.email,
    }


@router.get("/my-books")
def get_my_active_books(
    session: Annotated[Session, Depends(db_helper.session_getter)],
    user: UserRead = Depends(get_current_active_auth_user),
) -> Sequence[BorrowedBookInfo]:
    try:
        result = UserService.get_my_active_books(user.id, session)
    except ListBooksNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Active books not found."
        )

    return result


@router.get("/history")
def get_history_books(
    session: Annotated[Session, Depends(db_helper.session_getter)],
    user: UserRead = Depends(get_current_active_auth_user),
) -> Sequence[BorrowedBookWithDate]:
    try:
        result = UserService.get_history_books(user.id, session)
    except ListBooksNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="History is empty."
        )

    return result


@router.patch("/update-info")
def update_user(
    new_data: UserUpdate,
    session: Annotated[Session, Depends(db_helper.session_getter)],
    user: UserRead = Depends(get_current_active_auth_user),
) -> UserUpdate:
    try:
        UserService.update_user(new_data, user.id, session)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    return new_data


@router.delete("/delete-user")
def delete_user(
    user_id: int,
    session: Annotated[Session, Depends(db_helper.session_getter)],
    user: UserRead = Depends(get_current_active_auth_user),
) -> UserDelete:
    try:
        result = UserService.delete_user(
            user_id=user_id,
            self_id=user.id,
            session=session,
            raise_self_delete_exc=True,
        )
    except SelfDeleteException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot delete yourself, use /delete-me",
        )
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return result


@router.delete("/delete-me")
def delete_self(
    session: Annotated[Session, Depends(db_helper.session_getter)],
    user: UserRead = Depends(get_current_active_auth_user),
) -> UserDelete:
    try:
        result = UserService.delete_user(
            user_id=user.id,
            self_id=user.id,
            session=session,
        )
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return result


@router.get("/find-users")
def get_users(
    session: Annotated[Session, Depends(db_helper.session_getter)],
    id: Optional[int] = None,
) -> list[UserRead] | UserRead:
    try:
        result = UserService.get_users(
            id=id,
            session=session,
        )
    except ListUsersNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Users not found" if id is None else "User not found",
        )
    return result
