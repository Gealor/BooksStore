import asyncio
from core.models.base import Base
from core.models.db_helper import db_helper_mock

def drop_all_mock_table():
    Base.metadata.drop_all(bind=db_helper_mock.engine)
    print("Тестовые базы данных сброшены")

def create_all_mock_tables():
    Base.metadata.create_all(bind=db_helper_mock.engine)
    print("Тестовые базы данных созданы")


if __name__=="__main__":
    drop_all_mock_table()
    create_all_mock_tables()