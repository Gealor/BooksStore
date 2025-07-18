from typing import AsyncGenerator
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ):
        self.engine: Engine = create_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )

        self.session_factory: sessionmaker = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    # асинхронное отключение соединения от базы данных
    def dispose(self):
        self.engine.dispose()

    # получение сессии
    def session_getter(self):
        with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    url=settings.db.get_db_url(),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)

db_helper_mock = DatabaseHelper(
    url=settings.db_mock.get_db_url(),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
