from datetime import datetime
from typing import Sequence
from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import DatabaseError, IntegrityError

from core.models import Book
from core.schemas.books import BookCreate, BookDelete
from core.schemas.exceptions import InvalidDataError
from core.logger import log


class BookRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_all_books(
        self,
        include_deleted: bool = False,
    ) -> Sequence[Book]:
        stmt = select(Book).order_by(Book.id)
        if not include_deleted:
            stmt = stmt.where(Book.deleted_at.is_(None))

        result = self._session.scalars(stmt)
        return result.all()

    def get_book_by_id(
        self,
        book_id: int,
        include_deleted: bool = False,
    ) -> Book | None:
        stmt = select(Book).where(Book.id == book_id)
        if not include_deleted:
            stmt = stmt.where(Book.deleted_at.is_(None))
        result = self._session.scalar(stmt)
        return result

    def get_books_by_name(
        self,
        book_name: str,
        include_deleted: bool = False,
    ) -> Sequence[Book] | Book | None:
        stmt = select(Book).where(Book.title == book_name)
        if not include_deleted:
            stmt = stmt.where(Book.deleted_at.is_(None))
        result = self._session.scalars(stmt)

        return result.all()

    def get_books_by_author(
        self,
        author: str,
        include_deleted: bool = False,
    ) -> Sequence[Book]:
        stmt = select(Book).where(Book.author == author)
        if not include_deleted:
            stmt = stmt.where(Book.deleted_at.is_(None))
        result = self._session.scalars(stmt)

        return result.all()

    def get_books_by_isbn(
        self,
        isbn: str,
        include_deleted: bool = False,
    ) -> Book | None:
        stmt = select(Book).where(Book.ISBN == isbn)
        if not include_deleted:
            stmt = stmt.where(Book.deleted_at.is_(None))
        result = self._session.scalar(stmt)

        return result

    def create_book(
        self,
        book_create: BookCreate,
    ) -> Book:
        book = Book(**book_create.model_dump())
        self._session.add(book)
        try:
            self._session.commit()
        except (DatabaseError, IntegrityError):
            self._session.rollback()
            raise InvalidDataError
        return book

    def delete_book_by_id(
        self,
        book_id: int,
    ) -> BookDelete | None:
        stmt = update(Book).values(deleted_at = datetime.now()).where(Book.id==book_id).returning(Book.id, Book.deleted_at)

        try:
            result = self._session.execute(stmt).one_or_none()
        except IntegrityError as e:
            log.error("Database Exception: %s", e)
            self._session.rollback()
        self._session.commit()
        return BookDelete(book_id=result.id, deleted_at=result.deleted_at) if result else None 

    def update_book_data(
        self,
        book_id: int,
        new_data: dict,
    ) -> None:
        stmt = update(Book).values(**new_data).where(Book.id == book_id)
        try:
            self._session.execute(stmt)
        except (DatabaseError, IntegrityError):
            self._session.rollback()
            raise InvalidDataError
        self._session.commit()
        
