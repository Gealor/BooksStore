import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from core.models.base import Base
from core.models.db_helper import db_helper_mock
from core.config import settings


def create_database():
    conn = psycopg2.connect(
        # в dbname введите существующую базу данных в вашей СУБД, к которой можно подключиться
        dbname="postgres",
        user=settings.db_mock.user,
        password=settings.db_mock.password,
        host=settings.db_mock.host,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE {settings.db_mock.name}")
    print("База данных создана")
    cur.close()
    conn.close()


def drop_all_mock_table():
    Base.metadata.drop_all(bind=db_helper_mock.engine)
    print("Тестовые таблицы сброшены")


def create_all_mock_tables():
    Base.metadata.create_all(bind=db_helper_mock.engine)
    print("Тестовые таблицы созданы")


if __name__ == "__main__":
    create_database()
    drop_all_mock_table()
    create_all_mock_tables()
