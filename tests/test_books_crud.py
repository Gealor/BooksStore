from sqlalchemy import text
from core.schemas.books import BookCreate
from crud import books as books_crud
from core.models.db_helper import db_helper_mock

def clear_table_users(session):
    session.execute(text("TRUNCATE books CASCADE;"))
    session.execute(text("ALTER SEQUENCE books_id_seq RESTART WITH 1;"))
    session.commit()

with db_helper_mock.session_factory() as session:
    clear_table_users(session)


def test_create_books():
    book = BookCreate(
        title = "1984",
        author = "George Orwe",
        publication_year=1949,
        ISBN = "34521fghnbf",
        number_copies=4,
    )
    with db_helper_mock.session_factory() as session:
        result = books_crud.create_book(
            book,
            session,
        )

        assert result.title == "1984"
        assert result.author == 'George Orwe'

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
        result = books_crud.get_books_by_author("George Orwe", session)

    assert result is not None

def test_get_book_by_isbn():
    with db_helper_mock.session_factory() as session:
        result = books_crud.get_books_by_isbn("34521fghnbf", session)

    assert result is not None

def test_update_books_by_id():
    with db_helper_mock.session_factory() as session:
        user = books_crud.get_book_by_id(1, session)

        assert user is not None

        new_data = {
            "number_copies" : 2,
            "publication_year" : 1948
        }

        books_crud.update_book_data(user, new_data, session)


def test_delete_books():
    with db_helper_mock.session_factory() as session:
        result = books_crud.delete_book_by_id(1, session)