'''
Тестирование crud операций для users
Для корректного тестирования в терминале пропишите команду set PYTHONPATH=%CD%\\src !!!
'''
from sqlalchemy import text

from core.schemas.users import UserCreate
from crud import users as users_crud
from core.models.db_helper import db_helper_mock

def clear_table_users(session):
    session.execute(text("TRUNCATE users CASCADE;"))
    session.execute(text("ALTER SEQUENCE users_id_seq RESTART WITH 1;"))
    session.commit()

with db_helper_mock.session_factory() as session:
    clear_table_users(session)


def test_create_user():
    user = UserCreate(
        name = "John",
        email = "test1@mail.ru",
        password = "craft123",
    )
    with db_helper_mock.session_factory() as session:
        result = users_crud.create_user(
            user,
            session,
        )

        assert result.name == "John"
        assert result.email == 'test1@mail.ru'

def test_get_all_users():
    with db_helper_mock.session_factory() as session:
        result = users_crud.get_all_users(session)

    assert result is not None

def test_update_user_by_id():
    with db_helper_mock.session_factory() as session:
        user = users_crud.get_user_by_id(1, session)

        assert user is not None

        new_data = {
            "name" : "Gealor",
            "email" : "test2@gmail.com",
        }

        users_crud.update_user_data(user, new_data, session)


def test_delete_user():
    with db_helper_mock.session_factory() as session:
        result = users_crud.delete_user_by_id(1, session)


        
