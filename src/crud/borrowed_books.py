from typing import Sequence
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload, Session
from sqlalchemy.exc import DatabaseError

from core.models.books import Book
from core.models.borrowed_books import BorrowedBook
from core.schemas.borrowed_books import BorrowedBookCreate, BorrowedBookUpdate


def get_all_borrowed_books(
    session: Session,
) -> Sequence[BorrowedBook]:
    stmt = select(BorrowedBook).order_by(BorrowedBook.id)

    result = session.scalars(stmt)

    return result.all()


def get_borrowed_book_by_id(
    record_id: int,
    session: Session,
) -> BorrowedBook | None:
    stmt = select(BorrowedBook).where(BorrowedBook.id == record_id)

    result = session.scalar(stmt)

    return result


def get_active_borrowed_books_by_user_id(
    user_id,
    session: Session,
) -> Sequence[BorrowedBook]:
    stmt = select(BorrowedBook).where(
        and_(
            BorrowedBook.reader_id == user_id,
            BorrowedBook.return_date.is_(None),
        )
    )
    result = session.scalars(stmt)

    return result.all()


def get_history_about_books_by_user_id(
    user_id: int,
    session: Session,
) -> Sequence[BorrowedBook]:
    stmt = (
        select(BorrowedBook)
        .join(BorrowedBook.book)
        .options(selectinload(BorrowedBook.book))
        .where(BorrowedBook.reader_id == user_id)
        .order_by(BorrowedBook.borrow_date)
    )

    result = session.scalars(stmt)

    return result.all()


def get_active_borrowed_books_by_user_id(
    user_id: int,
    session: Session,
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
    result = session.scalars(stmt)

    return result.all()


def create_borrowed_book_record(
    record_create: BorrowedBookCreate,
    session: Session,
) -> BorrowedBook:
    record = BorrowedBook(**record_create.model_dump())

    session.add(record)
    session.commit()

    return record


def delete_borrowed_book_record(
    record_id: int,
    session: Session,
) -> int | None:
    stmt = select(BorrowedBook).where(BorrowedBook.id == record_id)

    record = session.scalar(stmt)
    if record:
        session.delete(record)
        session.commit()
    return record.id if record else None


def update_borrowed_book_record(
    record: BorrowedBook,
    record_update: BorrowedBookUpdate,
    session: Session,
) -> None:
    update = record_update.model_dump(exclude_defaults=False, exclude_unset=False)
    for key, value in update.items():
        setattr(record, key, value)

    session.commit()
