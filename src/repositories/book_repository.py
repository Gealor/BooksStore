from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import DatabaseError
from typing import Protocol

from core.models import Book
from core.schemas.books import BookCreate
from core.schemas.exceptions import InvalidDataError


class BookRepositoryAbstract(Protocol):
    def get_all_books(
        self,
    ) -> Sequence[Book]:
        pass

    def get_book_by_id(
        self,
        book_id: int,
    ) -> Book | None:
        pass

    def get_books_by_name(
        self,
        book_name: str,
    ) -> Sequence[Book] | Book | None:
        pass

    def get_books_by_author(
        self,
        author: str,
    ) -> Sequence[Book]:
        pass

    def get_books_by_isbn(
        self,
        isbn: str,
    ) -> Book | None:
        pass

    def create_book(
        self,
        book_create: BookCreate,
    ) -> Book:
        pass

    def delete_book_by_id(
        self,
        book_id: int,
    ) -> int | None:
        pass

    def update_book_data(
        self,
        book: Book,
        new_data: dict,
    ) -> None:
        pass


class BookRepository(BookRepositoryAbstract):
    def __init__(self, session: Session):
        self._session = session

    def get_all_books(
        self,
    ) -> Sequence[Book]:
        stmt = select(Book).order_by(Book.id)

        result = self._session.scalars(stmt)
        return result.all()

    def get_book_by_id(
        self,
        book_id: int,
    ) -> Book | None:
        stmt = select(Book).where(Book.id == book_id)
        result = self._session.scalar(stmt)
        return result

    def get_books_by_name(
        self,
        book_name: str,
    ) -> Sequence[Book] | Book | None:
        stmt = select(Book).where(Book.title == book_name)
        result = self._session.scalars(stmt)

        return result.all()

    def get_books_by_author(
        self,
        author: str,
    ) -> Sequence[Book]:
        stmt = select(Book).where(Book.author == author)
        result = self._session.scalars(stmt)

        return result.all()

    def get_books_by_isbn(
        self,
        isbn: str,
    ) -> Book | None:
        stmt = select(Book).where(Book.ISBN == isbn)
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
        except DatabaseError as e:
            self._session.rollback()
            raise InvalidDataError
        return book

    def delete_book_by_id(
        self,
        book_id: int,
    ) -> int | None:
        stmt = select(Book).where(Book.id == book_id)
        result = self._session.scalars(stmt)
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
            self._session.delete(book)
            # debug_session_objects(session)
            self._session.commit()
        else:
            self._session.rollback()
        return book.id if book else None

    def update_book_data(
        self,
        book: Book,
        new_data: dict,
    ) -> None:
        for key, value in new_data.items():
            setattr(book, key, value)
        try:
            self._session.commit()
        except DatabaseError:
            self._session.rollback()
            raise InvalidDataError
