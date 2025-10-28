# conftest.py файл для конфигурации тестирования и создания фикстур
from typing import Generator
import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from core.models.base import Base
from testcontainers.postgres import PostgresContainer
# то что указывается в качестве параметров тестов и фикстур, может быть другими фикстурами
# (чтобы передать фикстуру надо просто передать в качестве параметра ее имя, с которой она была определена)

@pytest.fixture(scope="session")
def postgres_container() -> Generator[PostgresContainer, None, None]:
    with PostgresContainer("postgres:15") as postgres:
        yield postgres


def create_db_url(postgres_container) -> str:
    raw_url = postgres_container.get_connection_url()
    return raw_url
    
@pytest.fixture(scope="session")
def engine(postgres_container) -> Generator[Engine, None, None]:
    """Create the database engine and tables once for the entire test session."""
    db_url = create_db_url(postgres_container)
    engine = create_engine(db_url)

    with engine.begin() as conn:
        Base.metadata.create_all(conn)

    yield engine

    engine.dispose()

@pytest.fixture(scope="function")
def session(engine) -> Generator[Session, None, None]:
    """Creates a new session and rolls back all changes for full test isolation."""
    session_factory = sessionmaker(
        engine, expire_on_commit=False, class_=Session
    )
    connection = engine.connect()  # Get a new DB connection
    transaction = connection.begin()  # Start an outer transaction

    session = session_factory(bind=connection)  # Bind session to this connection
    session.begin_nested()  # Begin a SAVEPOINT for test isolation

    try:
        yield session  # Test runs inside this session
    finally:
        session.rollback()  # Rollback all changes made by the test
        transaction.rollback()  # Ensure the outer transaction is also rolled back
        connection.close()  # Close connection after test completion
        session.close()  # Explicitly close the session
