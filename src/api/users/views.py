
from typing import Annotated, Optional, Sequence
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.auth.tools.tools_auth import get_current_active_auth_user
from core.models import db_helper
from core.schemas.books import BookRead
from core.schemas.borrowed_books import BorrowedBookInfo, BorrowedBookWithDate
from core.schemas.user import UserBase, UserDelete, UserRead, UserUpdate
from core.config import settings
from crud import users as users_crud
from crud import borrowed_books as bb_crud


router = APIRouter(
    prefix = settings.api.users.prefix,
    tags = ["Users"]
    )

@router.get('/me')
def auth_user_check_self_info(
    user : UserRead = Depends(get_current_active_auth_user)
) -> UserBase:
    return {
        "name" : user.name,
        "email" : user.email,
    }

@router.get('/my-books')
def get_my_active_books(
    session : Annotated[Session, Depends(db_helper.session_getter)],
    user : UserRead = Depends(get_current_active_auth_user)
) -> Sequence[BorrowedBookInfo]:
    result = bb_crud.get_active_borrowed_books_by_user_id(user.id, session)

    return result

@router.get('/history')
def get_history_books(
    session : Annotated[Session, Depends(db_helper.session_getter)],
    user : UserRead = Depends(get_current_active_auth_user),
) -> Sequence[BorrowedBookWithDate]:
    result = bb_crud.get_history_about_books_by_user_id(user.id, session)

    return result


@router.patch('/update-info')
def update_user(
    new_data : UserUpdate,
    session : Annotated[Session, Depends(db_helper.session_getter)],
    user : UserRead = Depends(get_current_active_auth_user),
) -> UserUpdate:
    id = int(user.id)

    found_user = users_crud.get_user_by_id(id, session)
    
    values_dict = new_data.model_dump(exclude_unset=True)
    users_crud.update_user_data(found_user, values_dict, session)
    return new_data

@router.delete('/delete-user')
def delete_user(
    user_id : int,
    session : Annotated[Session, Depends(db_helper.session_getter)],
    user : UserRead = Depends(get_current_active_auth_user)
) -> UserDelete:
    if user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail = "You cannot delete yourself, use /delete-me"
        )
    deleted_id = users_crud.delete_user_by_id(user_id, session)
    if deleted_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "User not found",
        )
    return {
        "deleted" : deleted_id,
    }

@router.delete('/delete-me')
def delete_self(
    session : Annotated[Session, Depends(db_helper.session_getter)],
    user : UserRead = Depends(get_current_active_auth_user)
)-> UserDelete:
    deleted_id = users_crud.delete_user_by_id(user.id, session)
    return {
        "deleted" : deleted_id,
    }

@router.get('/find-users')
def get_users(
    session : Annotated[Session, Depends(db_helper.session_getter)],
    id : Optional[int] = None,
) -> list[UserRead] | UserRead:
    users = users_crud.get_all_users(session = session) if id is None else users_crud.get_user_by_id(id, session)
    if users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Users not found" if id is None else "User not found"
        )
    return users


