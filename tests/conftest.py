# conftest.py файл для конфигурации тестирования и создания фикстур
import pytest
from sqlalchemy import text
from core.schemas.books import BookCreate
from core.schemas.users import UserCreate
from core.models import db_helper_mock, db_helper
from crud import users as users_crud
from crud import books as books_crud
from create_mock_database import create_all_mock_tables
from create_mock_database import drop_all_mock_table

list_users = [
    {
        "name": "Иван Петров",
        "email": "ivan.petrov@example.com",
        "password": "Petrov2025!",
    },
    {
        "name": "Мария Смирнова",
        "email": "maria.smirnova@example.org",
        "password": "Sm1rnova#88",
    },
    {
        "name": "Алексей Кузнецов",
        "email": "aleksey.kuznetsov@domain.ru",
        "password": "Kuznecov_77",
    },
    {
        "name": "Екатерина Волкова",
        "email": "ekaterina.volkova@mail.com",
        "password": "Volkova!2024",
    },
    {
        "name": "Дмитрий Соколов",
        "email": "dmitriy.sokolov@inbox.ru",
        "password": "SokolovPass9",
    },
]

list_books = [
    {
        "title": "Мастер и Маргарита",
        "author": "Михаил Булгаков",
        "ISBN": "9780141180144",
        "publication_year": 1967,
        "number_copies": 3,
    },
    {
        "title": "Преступление и наказание",
        "author": "Фёдор Достоевский",
        "ISBN": "9785170793316",
        "publication_year": 1866,
        "number_copies": 5,
    },
    {
        "title": "Война и мир",
        "author": "Лев Толстой",
        "ISBN": "9780140447934",
        "publication_year": 1869,
        "number_copies": 2,
    },
    {
        "title": "1984",
        "author": "Джордж Оруэлл",
        "ISBN": "9780451524935",
        "publication_year": 1949,
        "number_copies": 4,
    },
    {"title": "Улисс", "author": "Джеймс Джойс", "number_copies": 1},
]


# фикстура, которая выполняется на уровне сессии(т.е. один раз за сессию тестирования) и применяется ко всем тестам без явного указания
@pytest.fixture(scope="session", autouse=True)
def fill_and_clear_databases():
    drop_all_mock_table()
    create_all_mock_tables()
    with db_helper_mock.session_factory() as session:
        for user in list_users:
            user_model = UserCreate(**user)
            result = users_crud.create_user(
                user_model,
                session,
            )
        for book in list_books:
            book_model = BookCreate(**book)
            result = books_crud.create_book(
                book_model,
                session,
            )
    yield
    pass
    with db_helper_mock.session_factory() as session:
        session.execute(text("TRUNCATE users, books, borrowed_books CASCADE;"))
        session.execute(text("ALTER SEQUENCE users_id_seq RESTART WITH 1;"))
        session.execute(text("ALTER SEQUENCE books_id_seq RESTART WITH 1;"))
        session.execute(text("ALTER SEQUENCE borrowed_books_id_seq RESTART WITH 1;"))
        session.commit()
