from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.models.books import Book
from core.schemas.exceptions import InvalidDataError
from crud import borrowed_books as bb_crud
from crud import books as books_crud
from core.config import settings


def check_availability_book(record, user_id) -> None:
    if record.reader_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found in your library",
        )


def check_record_found(record) -> None:
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )


def check_number_copies(book: Book) -> None:
    if book.number_copies == 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not available"
        )


def check_number_of_active_books_user(
    user_id: int,
    max_active_books: int,
    session: Session,
) -> None:
    records = bb_crud.get_active_borrowed_books_by_user_id(user_id, session)
    if len(records) == max_active_books:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Maximum number of books borrowed : {settings.business.max_active_books}",
        )


def check_return_book(record) -> None:
    if record.return_date is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Book already return",
        )


def reduce_number_of_copies(
    book: Book,
    session: Session,
):
    new_data = {"number_copies": book.number_copies - 1}
    try:
        books_crud.update_book_data(book, new_data, session)
    except InvalidDataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data.",
        )


def increase_number_of_copies(
    book: Book,
    session: Session,
):
    new_data = {"number_copies": book.number_copies + 1}
    try:
        books_crud.update_book_data(book, new_data, session)
    except InvalidDataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data.",
        )
