from typing import Protocol, Sequence
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload, Session
from sqlalchemy.exc import DatabaseError

from core.models.books import Book
from core.models.borrowed_books import BorrowedBook
from core.schemas.borrowed_books import BorrowedBookCreate, BorrowedBookUpdate


class BorrowedBookRepositoryAbstract(Protocol):
    def get_all_borrowed_books(self) -> Sequence[BorrowedBook]:
        pass

    def get_borrowed_book_by_id(
        self,
        record_id: int,
    ) -> BorrowedBook | None:
        pass

    def get_active_borrowed_books_by_user_id(
        self,
        user_id,
    ) -> Sequence[BorrowedBook]:
        pass

    def get_history_about_books_by_user_id(
        self,
        user_id: int,
    ) -> Sequence[BorrowedBook]:
        pass

    def get_active_borrowed_books_by_user_id(
        self,
        user_id: int,
    ) -> Sequence[BorrowedBook]:
        pass

    def create_borrowed_book_record(
        self,
        record_create: BorrowedBookCreate,
    ) -> BorrowedBook:
        pass

    def delete_borrowed_book_record(
        self,
        record_id: int,
    ) -> int | None:
        pass

    def update_borrowed_book_record(
        self,
        record: BorrowedBook,
        record_update: BorrowedBookUpdate,
    ) -> None:
        pass


class BorrowedBookRepository(BorrowedBookRepositoryAbstract):
    def __init__(self, session: Session):
        self._session = session

    def get_all_borrowed_books(self) -> Sequence[BorrowedBook]:
        stmt = select(BorrowedBook).order_by(BorrowedBook.id)

        result = self._session.scalars(stmt)

        return result.all()

    def get_borrowed_book_by_id(
        self,
        record_id: int,
    ) -> BorrowedBook | None:
        stmt = select(BorrowedBook).where(BorrowedBook.id == record_id)

        result = self._session.scalar(stmt)

        return result

    def get_active_borrowed_books_by_user_id(
        self,
        user_id,
    ) -> Sequence[BorrowedBook]:
        stmt = select(BorrowedBook).where(
            and_(
                BorrowedBook.reader_id == user_id,
                BorrowedBook.return_date.is_(None),
            )
        )
        result = self._session.scalars(stmt)

        return result.all()

    def get_history_about_books_by_user_id(
        self,
        user_id: int,
    ) -> Sequence[BorrowedBook]:
        stmt = (
            select(BorrowedBook)
            .join(BorrowedBook.book)
            .options(selectinload(BorrowedBook.book))
            .where(BorrowedBook.reader_id == user_id)
            .order_by(BorrowedBook.borrow_date)
        )

        result = self._session.scalars(stmt)

        return result.all()

    def get_active_borrowed_books_by_user_id(
        self,
        user_id: int,
    ) -> Sequence[BorrowedBook]:
        # нельзя в select указать BorrowedBook.book, т.к. мы подгружаем данные(с помощью options) для таблицы BorrowedBooks
        # если надо использовать именно BorrowedBook.book надо убрать options и использовать join(уже есть)
        stmt = (
            select(BorrowedBook)
            .join(BorrowedBook.book)
            .options(selectinload(BorrowedBook.book))
            .where(
                and_(
                    BorrowedBook.reader_id == user_id,
                    BorrowedBook.return_date.is_(None),
                )
            )
        )
        result = self._session.scalars(stmt)

        return result.all()

    def create_borrowed_book_record(
        self,
        record_create: BorrowedBookCreate,
    ) -> BorrowedBook:
        record = BorrowedBook(**record_create.model_dump())

        self._session.add(record)
        self._session.commit()

        return record

    def delete_borrowed_book_record(
        self,
        record_id: int,
    ) -> int | None:
        stmt = select(BorrowedBook).where(BorrowedBook.id == record_id)

        record = self._session.scalar(stmt)
        if record:
            self._session.delete(record)
            self._session.commit()
        return record.id if record else None

    def update_borrowed_book_record(
        self,
        record: BorrowedBook,
        record_update: BorrowedBookUpdate,
    ) -> None:
        update = record_update.model_dump(exclude_defaults=False, exclude_unset=False)
        for key, value in update.items():
            setattr(record, key, value)

        self._session.commit()
