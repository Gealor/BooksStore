from fastapi import APIRouter
from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.tools_auth import get_current_active_auth_user
from core.config import settings
from core.models import db_helper
from core.schemas.exceptions import BookNotFoundException, InvalidDataError
from core.schemas.users import UserRead
from core.schemas.books import BookCreate, BookDelete, BookRead, BookUpdate
from services.book_service import BookService

router = APIRouter(
    prefix=settings.api.books.prefix,
    tags=["Books"],
)


@router.get("/library")
def get_all_books(
    session: Annotated[Session, Depends(db_helper.session_getter)],
) -> list[BookRead]:
    books = BookService(session=session).get_all_books()
    return books


@router.post("/add-book")
def create_book(
    book_create: BookCreate,
    session: Annotated[Session, Depends(db_helper.session_getter)],
    user: UserRead = Depends(get_current_active_auth_user),
) -> BookRead:
    try:
        book = BookService(session=session).create_book(book_create)
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
    try:
        result = BookService(session=session).update_book_by_id(book_id, book_update)
    except BookNotFoundException:
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    except InvalidDataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data",
        )
    return result


@router.delete("/delete-book")
def delete_book_by_id(
    book_id: int,
    session: Annotated[Session, Depends(db_helper.session_getter)],
    user: UserRead = Depends(get_current_active_auth_user),
) -> BookDelete:
    try:
        result = BookService(session=session).delete_book_by_id(book_id)
    except BookNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    return result
