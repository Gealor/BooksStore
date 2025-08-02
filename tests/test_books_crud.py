from pydantic import ValidationError
import pytest
from sqlalchemy import text
from core.schemas.books import BookCreate, BookUpdate
from core.models.db_helper import db_helper_mock
from repositories.book_repository import BookRepository


def test_create_book():
    book = BookCreate(
        title="Билли Саммерс",
        author="Стивен Кинг",
        publication_year=2021,
        ISBN="123456789abcd",
        number_copies=4,
    )
    with db_helper_mock.session_factory() as session:
        result = BookRepository(session=session).create_book(book)

        assert result.title == "Билли Саммерс"
        assert result.author == "Стивен Кинг"


def test_get_all_books():
    with db_helper_mock.session_factory() as session:
        result = BookRepository(session=session).get_all_books()

    assert result is not None


def test_get_book_by_id():
    with db_helper_mock.session_factory() as session:
        result = BookRepository(session=session).get_book_by_id(1)

    assert result is not None


def test_get_book_by_title():
    with db_helper_mock.session_factory() as session:
        result = BookRepository(session=session).get_books_by_name("1984")

    assert result is not None


def test_get_book_by_author():
    with db_helper_mock.session_factory() as session:
        result = BookRepository(session=session).get_books_by_author("Джордж Оруэлл")

    assert result is not None


def test_get_book_by_isbn():
    with db_helper_mock.session_factory() as session:
        result = BookRepository(session=session).get_books_by_isbn("123456789abcd")

    assert result is not None


def test_update_books_by_id():
    with db_helper_mock.session_factory() as session:
        book = BookRepository(session=session).get_book_by_id(1)

        assert book is not None

        book_update = BookUpdate(
            number_copies=2,
            publication_year=1948,
        )
        new_data = book_update.model_dump(exclude_unset=True)

        BookRepository(session=session).update_book_data(book, new_data)


def test_invalid_update_book():
    with pytest.raises(ValidationError):
        with db_helper_mock.session_factory() as session:
            book = BookRepository(session=session).get_book_by_id(1)

            assert book is not None

            book_update = BookUpdate(
                number_copies=-2,
                publication_year=-2,
            )
            new_data = book_update.model_dump(exclude_unset=True)

            BookRepository(session=session).update_book_data(book, new_data)


def test_delete_books():
    with db_helper_mock.session_factory() as session:
        result = BookRepository(session=session).delete_book_by_id(1)

        assert result is not None


def test_delete_books_2():
    with db_helper_mock.session_factory() as session:
        result = BookRepository(session=session).delete_book_by_id(2)

        assert result is not None
