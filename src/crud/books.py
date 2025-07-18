from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import selectinload, Session
from sqlalchemy.exc import DatabaseError

from auth import tools as auth_tools
from core.models import Book
from core.schemas.books import BookCreate, BookRead
from core.schemas.exceptions import InvalidDataError
from core.models.borrowed_books import BorrowedBook
from core.models.users import User


def get_all_books(
    session: Session,
) -> Sequence[Book]:
    stmt = select(Book).order_by(Book.id)

    result = session.scalars(stmt)
    return result.all()


def get_book_by_id(
    book_id: int,
    session: Session,
) -> Book | None:
    stmt = select(Book).where(Book.id == book_id)
    result = session.scalar(stmt)
    return result


def get_books_by_name(
    book_name: str,
    session: Session,
) -> Sequence[Book] | Book | None:
    stmt = select(Book).where(Book.title == book_name)
    result = session.scalars(stmt)

    return result.all()


def get_books_by_author(
    author: str,
    session: Session,
) -> Sequence[Book]:
    stmt = select(Book).where(Book.author == author)
    result = session.scalars(stmt)

    return result.all()


def get_books_by_isbn(
    isbn: str,
    session: Session,
) -> Book | None:
    stmt = select(Book).where(Book.ISBN == isbn)
    result = session.scalar(stmt)

    return result


def create_book(
    book_create: BookCreate,
    session: Session,
) -> Book:

    book = Book(**book_create.model_dump())
    session.add(book)
    try:
        session.commit()
    except DatabaseError as e:
        session.rollback()
        raise InvalidDataError
    return book


def delete_book_by_id(
    book_id: int,
    session: Session,
) -> int | None:
    stmt = select(Book).where(Book.id == book_id)
    result = session.scalars(stmt)
    book = result.one_or_none()
    # def debug_session_objects(session):
    #     print("Session contains:")
    #     for obj in session.identity_map.values():
    #         if isinstance(obj, User):
    #             print("  User in session:", obj.id, "Borrowed books:", [bb.id for bb in obj.borrowed_books])
    #         elif isinstance(obj, Book):
    #             print("  Book in session:", obj.id)
    #         elif isinstance(obj, BorrowedBook):
    #             print("  BorrowedBook in session:", obj.id, "book_id:", obj.book_id, "reader_id:", obj.reader_id)

    if book:
        session.delete(book)
        # debug_session_objects(session)
        session.commit()
    return book.id if book else None


def update_book_data(
    book: Book,
    new_data: dict,
    session: Session,
) -> None:
    for key, value in new_data.items():
        setattr(book, key, value)
    try:
        session.commit()
    except DatabaseError:
        session.rollback()
        raise InvalidDataError
