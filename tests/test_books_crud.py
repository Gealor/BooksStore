from pydantic import ValidationError
import pytest
from sqlalchemy import text
from core.schemas.books import BookCreate, BookUpdate
from crud import books as books_crud
from core.models.db_helper import db_helper_mock


def test_create_book():
    book = BookCreate(
        title="Билли Саммерс",
        author="Стивен Кинг",
        publication_year=2021,
        ISBN="123456789abcd",
        number_copies=4,
    )
    with db_helper_mock.session_factory() as session:
        result = books_crud.create_book(
            book,
            session,
        )

        assert result.title == "Билли Саммерс"
        assert result.author == "Стивен Кинг"


def test_get_all_books():
    with db_helper_mock.session_factory() as session:
        result = books_crud.get_all_books(session)

    assert result is not None


def test_get_book_by_id():
    with db_helper_mock.session_factory() as session:
        result = books_crud.get_book_by_id(1, session)

    assert result is not None


def test_get_book_by_title():
    with db_helper_mock.session_factory() as session:
        result = books_crud.get_books_by_name("1984", session)

    assert result is not None


def test_get_book_by_author():
    with db_helper_mock.session_factory() as session:
        result = books_crud.get_books_by_author("Джордж Оруэлл", session)

    assert result is not None


def test_get_book_by_isbn():
    with db_helper_mock.session_factory() as session:
        result = books_crud.get_books_by_isbn("123456789abcd", session)

    assert result is not None


def test_update_books_by_id():
    with db_helper_mock.session_factory() as session:
        book = books_crud.get_book_by_id(1, session)

        assert book is not None

        book_update = BookUpdate(
            number_copies=2,
            publication_year=1948,
        )
        new_data = book_update.model_dump(exclude_unset=True)

        books_crud.update_book_data(book, new_data, session)


def test_invalid_update_book():
    with pytest.raises(ValidationError):
        with db_helper_mock.session_factory() as session:
            book = books_crud.get_book_by_id(1, session)

            assert book is not None

            book_update = BookUpdate(
                number_copies=-2,
                publication_year=-2,
            )
            new_data = book_update.model_dump(exclude_unset=True)

            books_crud.update_book_data(book, new_data, session)


def test_delete_books():
    with db_helper_mock.session_factory() as session:
        result = books_crud.delete_book_by_id(1, session)


def test_delete_books_2():
    with db_helper_mock.session_factory() as session:
        result = books_crud.delete_book_by_id(2, session)
