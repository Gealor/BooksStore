import pytest
from sqlalchemy.orm import Session

from core.models.books import Book
from core.models.users import User


@pytest.fixture
def mock_users(session: Session):
    list_users = [
        User(
            name="Иван Петров",
            email="ivan.petrov@example.com",
            password="Petrov2025!",
        ),
        User(
            name="Мария Смирнова",
            email="maria.smirnova@example.org",
            password="Sm1rnova#88",
        ),
        User(
            name="Алексей Кузнецов",
            email="aleksey.kuznetsov@domain.ru",
            password="Kuznecov_77",
        ),
        User(
            name="Екатерина Волкова",
            email="ekaterina.volkova@mail.com",
            password="Volkova!2024",
        ),
        User(
            name="Дмитрий Соколов",
            email="dmitriy.sokolov@inbox.ru",
            password="SokolovPass9",
        ),
    ]

    session.add_all(list_users)
    session.commit()
    return list_users

@pytest.fixture
def mock_books(session: Session):
    list_books = [
        Book(
            title="Мастер и Маргарита",
            author="Михаил Булгаков",
            ISBN="9780141180144",
            publication_year=1967,
            number_copies=3,
        ),
        Book(
            title="Преступление и наказание",
            author="Фёдор Достоевский",
            ISBN="9785170793316",
            publication_year=1866,
            number_copies=5,
        ),
        Book(
            title="Война и мир",
            author="Лев Толстой",
            ISBN="9780140447934",
            publication_year=1869,
            number_copies=2,
        ),
        Book(
            title="1984",
            author="Джордж Оруэлл",
            ISBN="9780451524935",
            publication_year=1949,
            number_copies=4,
        ),
        Book(
            title="Улисс",
            author="Джеймс Джойс",
            ISBN="9784561556036",
            publication_year=1918,
            number_copies=1,
        ),
    ]

    session.add_all(list_books)
    session.commit()
    return list_books