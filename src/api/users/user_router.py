from typing import Annotated, Optional, Sequence
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.tools_auth import auth_wrapper
from core.models import db_helper
from core.schemas.borrowed_books import BorrowedBookInfo, BorrowedBookWithDate
from core.schemas.exceptions import ListBooksNotFoundException, ListUsersNotFoundException, SelfDeleteException, UserNotFoundException
from core.schemas.users import UserBase, UserDelete, UserRead, UserUpdate
from core.config import settings
from services.user_service import UserService


router = APIRouter(prefix=settings.api.users.prefix, tags=["Users"])


@router.get("/me")
def auth_user_check_self_info(
    user: UserRead = Depends(auth_wrapper),
) -> UserBase:
    return {
        "name": user.name,
        "email": user.email,
    }


@router.get("/my_books")
def get_my_active_books(
    session: Annotated[Session, Depends(db_helper.session_getter)],
    user: UserRead = Depends(auth_wrapper),
) -> Sequence[BorrowedBookInfo]:
    try:
        result = UserService(session=session).get_my_active_books(user.id)
    except ListBooksNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Active books not found."
        )

    return result


@router.get("/history")
def get_history_books(
    session: Annotated[Session, Depends(db_helper.session_getter)],
    user: UserRead = Depends(auth_wrapper),
) -> Sequence[BorrowedBookWithDate]:
    try:
        result = UserService(session=session).get_history_books(user.id)
    except ListBooksNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="History is empty."
        )

    return result


@router.patch("/update")
def update_user(
    new_data: UserUpdate,
    session: Annotated[Session, Depends(db_helper.session_getter)],
    user: UserRead = Depends(auth_wrapper),
) -> UserUpdate:
    try:
        UserService(session=session).update_user(new_data, user.id)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    return new_data


@router.delete("/delete")
def delete_user(
    user_id: int,
    session: Annotated[Session, Depends(db_helper.session_getter)],
    user: UserRead = Depends(auth_wrapper),
) -> UserDelete:
    try:
        result = UserService(session=session).delete_user(
            user_id=user_id,
            self_id=user.id,
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


@router.delete("/delete_self")
def delete_self(
    session: Annotated[Session, Depends(db_helper.session_getter)],
    user: UserRead = Depends(auth_wrapper),
) -> UserDelete:
    try:
        result = UserService(session=session).delete_user(
            user_id=user.id,
            self_id=user.id,
        )
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return result


@router.get("/users")
def get_users(
    session: Annotated[Session, Depends(db_helper.session_getter)],
    include_deleted: bool = False,
) -> list[UserRead] | UserRead:
    try:
        result = UserService(session=session).get_users(
            include_deleted=include_deleted,
        )
    except ListUsersNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Users not found",
        )
    return result

@router.get("/user/{user_id}")
def get_user_by_id(
    session: Annotated[Session, Depends(db_helper.session_getter)],
    user_id: int,
    include_deleted: bool = False,
) -> UserRead:
    try:
        result = UserService(session=session).get_user_by_id(
            id=user_id,
            include_deleted=include_deleted
        )
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return result