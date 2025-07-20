"""
Тестирование crud операций для users
Для корректного тестирования в терминале пропишите команду set PYTHONPATH=%CD%\\src !!!
"""

from pydantic import ValidationError
import pytest
from sqlalchemy import text

from core.schemas.users import UserCreate, UserUpdate
from crud import users as users_crud
from core.models.db_helper import db_helper_mock
from repositories.user_repository import UserRepository


def test_create_user():
    user = UserCreate(
        name="Максим",
        email="test1@mail.ru",
        password="craft123",
    )
    with db_helper_mock.session_factory() as session:
        result = UserRepository(session=session).create_user(user)

        assert result.name == "Максим"
        assert result.email == "test1@mail.ru"


def test_get_all_users():
    with db_helper_mock.session_factory() as session:
        result = UserRepository(session=session).get_all_users()

    assert result is not None


def test_update_user_by_id():
    with db_helper_mock.session_factory() as session:
        user = UserRepository(session=session).get_user_by_id(4)

        assert user is not None

        user_data = UserUpdate(
            name="Gealor",
            email="test2@gmail.com",
        )

        new_data = user_data.model_dump(exclude_unset=True)

        UserRepository(session=session).update_user_data(user, new_data)


def test_delete_user():
    with db_helper_mock.session_factory() as session:
        result = UserRepository(session=session).delete_user_by_id(4)


def test_invalid_update_user_data():
    with pytest.raises(ValidationError):
        with db_helper_mock.session_factory() as session:
            user = UserRepository(session=session).get_user_by_id(2)

            assert user is not None

            user_data = UserUpdate(name="Gealor", password="1")
            new_data = user_data.model_dump(exclude_unset=True)

            UserRepository(session=session).update_user_data(user, new_data)
