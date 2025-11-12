from unittest.mock import MagicMock
import pytest
from core.models.users import User
from services.user_service import UserService


@pytest.fixture
def mock_users_list():
    list_users = [
        User(
            id=1,
            name="Иван Петров",
            email="ivan.petrov@example.com",
            password="Petrov2025!",
        ),
        User(
            id=2,
            name="Мария Смирнова",
            email="maria.smirnova@example.org",
            password="Sm1rnova#88",
        ),
        User(
            id=3,
            name="Алексей Кузнецов",
            email="aleksey.kuznetsov@domain.ru",
            password="Kuznecov_77",
        ),
        User(
            id=4,
            name="Екатерина Волкова",
            email="ekaterina.volkova@mail.com",
            password="Volkova!2024",
        ),
        User(
            id=5,
            name="Дмитрий Соколов",
            email="dmitriy.sokolov@inbox.ru",
            password="SokolovPass9",
        ),
    ]
    return list_users

@pytest.fixture
def mock_user_repo(mocker):
    mock_repo = mocker.MagicMock()
    mocker.patch("services.user_service.UserRepository", return_value=mock_repo)
    return mock_repo

@pytest.fixture
def mock_borrowed_books_repo(mocker):
    mock_repo = mocker.MagicMock()
    mocker.patch("services.user_service.BorrowedBookRepository", return_value=mock_repo)
    return mock_repo

@pytest.fixture
def user_service():
    session_mock = MagicMock()
    service = UserService(session=session_mock)

    return service

# TODO: добавить тесты для сервисов Book и BorrowedBooks