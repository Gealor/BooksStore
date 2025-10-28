import pytest
from core.models.books import Book, BorrowedBook
from sqlalchemy.orm import Session

from core.models.users import User
from core.schemas.borrowed_books import BorrowedBookUpdate
from repositories.borrowed_book_repository import BorrowedBookRepository

@pytest.fixture
def borrowed_book_repo(session: Session):
    return BorrowedBookRepository(session=session)

@pytest.fixture
def test_user(session: Session):
    user = User(
        id=1,
        name="Иван Петров",
        email="ivan.petrov@example.com",
        password="Petrov2025!",
    )
    session.add(user)
    return user

@pytest.fixture
def test_book(session: Session):
    book = Book(
        id=1,
        title="Мастер и Маргарита",
        author="Михаил Булгаков",
        ISBN="9780141180144",
        publication_year=1967,
        number_copies=3,
    )
    session.add(book)
    return book

@pytest.fixture
def mock_records(session: Session, mock_books, test_user):
    list_records = [
        BorrowedBook(id=1, book_id=mock_books[0].id, reader_id=test_user.id),
        BorrowedBook(id=2, book_id=mock_books[1].id, reader_id=test_user.id),
        BorrowedBook(id=3, book_id=mock_books[2].id, reader_id=test_user.id),
    ]
    session.add_all(list_records)
    return list_records

@pytest.fixture
def update_record():
    return BorrowedBookUpdate()

def test_create_book(borrowed_book_repo, test_user, test_book):
    result = borrowed_book_repo.create_borrowed_book_record(
        book_id=test_book.id,
        reader_id=test_user.id
    )

    assert result is not None

    record = borrowed_book_repo.get_borrowed_book_by_id(record_id=result.id)

    assert record is not None
    assert result.id == record.id

def test_get_all_borrowed_books(borrowed_book_repo, mock_records):
    result = borrowed_book_repo.get_all_borrowed_books()

    assert len(result) == len(mock_records)

def test_get_borrowed_book_by_id_successful(borrowed_book_repo, mock_records):
    result = borrowed_book_repo.get_borrowed_book_by_id(record_id=mock_records[0].id)

    assert result is not None

def test_get_borrowed_book_by_id_not_found(borrowed_book_repo, mock_records):
    result = borrowed_book_repo.get_borrowed_book_by_id(record_id=10)

    assert result is None

def test_update_borrowed_book_record(borrowed_book_repo, update_record, mock_records):
    result = borrowed_book_repo.get_borrowed_book_by_id(record_id=mock_records[0].id)

    assert result.return_date is None

    borrowed_book_repo.update_borrowed_book_record(result, update_record)

    assert result.return_date is not None
