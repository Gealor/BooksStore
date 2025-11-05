from unittest.mock import MagicMock
import pytest
from core.models.users import User
from services.user_service import UserService


@pytest.fixture
def mock_users_list():
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
    return list_users

@pytest.fixture
def user_service():
    session_mock = MagicMock()
    service = UserService(session=session_mock)
    return service