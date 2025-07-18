from fastapi import APIRouter
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.auth.tools.tools_auth import get_current_active_auth_user
from core.config import settings
from core.models import db_helper
from core.schemas.exceptions import InvalidDataError
from core.schemas.users import UserRead
from crud import books as books_crud
from core.schemas.books import BookCreate, BookDelete, BookRead, BookUpdate

router = APIRouter(
    prefix=settings.api.books.prefix,
    tags=["Books"],
)


@router.get("/library")
def get_all_books(
    session: Annotated[Session, Depends(db_helper.session_getter)],
) -> list[BookRead]:
    books = books_crud.get_all_books(session)

    return books


@router.post("/add-book")
def create_book(
    book_create: BookCreate,
    session: Annotated[Session, Depends(db_helper.session_getter)],
    user: UserRead = Depends(get_current_active_auth_user),
) -> BookRead:
    try:
        book = books_crud.create_book(book_create, session)
    except InvalidDataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data",
        )
    return book


@router.patch("/update-book")
def update_book_by_id(
    book_id: int,
    book_update: BookUpdate,
    session: Annotated[Session, Depends(db_helper.session_getter)],
    user: UserRead = Depends(get_current_active_auth_user),
) -> BookUpdate:

    found_book = books_crud.get_book_by_id(book_id, session)
    if found_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    values_dict = book_update.model_dump(exclude_unset=True)
    try:
        books_crud.update_book_data(found_book, values_dict, session)
    except InvalidDataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data",
        )
    return book_update


@router.delete("/delete-book")
def delete_book_by_id(
    book_id: int,
    session: Annotated[Session, Depends(db_helper.session_getter)],
    user: UserRead = Depends(get_current_active_auth_user),
) -> BookDelete:
    deleted_id = books_crud.delete_book_by_id(book_id, session)
    if deleted_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    return {
        "deleted": deleted_id,
    }
