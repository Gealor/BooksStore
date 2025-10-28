import pytest
from core.models.books import Book
from sqlalchemy.orm import Session

from core.schemas.books import BookCreate, BookUpdate
from repositories.book_repository import BookRepository

@pytest.fixture
def book_repo(session: Session):
    return BookRepository(session=session)

@pytest.fixture
def create_book():
    return BookCreate(
        title="Собачье Сердце",
        author="Михаил Булгаков",
        ISBN="123456789abcd",
        publication_year=1968,
        number_copies=5
    )

@pytest.fixture
def update_book():
    return BookUpdate(
        publication_year=2000,
        description="Что-то"
    )

def test_get_all_books(book_repo, mock_books):
    result = book_repo.get_all_books()

    assert len(result) == len(mock_books)

def test_get_book_by_id_successful(book_repo, mock_books):
    result = book_repo.get_book_by_id(book_id=mock_books[0].id)

    assert result is not None
    assert result.id == mock_books[0].id
    assert result.title == mock_books[0].title

def test_get_book_by_id_not_found(book_repo, mock_books):
    result = book_repo.get_book_by_id(book_id=45)

    assert result is None

def test_get_book_by_name_successful(book_repo, mock_books):
    result = book_repo.get_books_by_name(book_name=mock_books[0].title)

    assert result is not None
    assert len(result) == 1
    assert result[0].title == mock_books[0].title

def test_get_book_by_name_not_found(book_repo, mock_books):
    result = book_repo.get_books_by_name(book_name="Something")

    assert not result

def test_create_book(book_repo, mock_books, create_book):
    created_book = book_repo.create_book(book_create=create_book)

    book = book_repo.get_books_by_name(book_name=create_book.title)

    assert created_book.id == book[0].id
    assert created_book.title == book[0].title

def test_delete_book_by_id(book_repo, mock_books, create_book):
    book = book_repo.get_book_by_id(book_id=mock_books[0].id)

    assert book is not None

    deleted_book_id = book_repo.delete_book_by_id(book_id=mock_books[0].id)

    assert deleted_book_id is not None
    assert deleted_book_id == book.id
    
    book = book_repo.get_book_by_id(book_id=mock_books[0].id)
    assert book is None

def test_update_book_by_id(book_repo, update_book, mock_books):
    book = book_repo.get_book_by_id(book_id=mock_books[0].id)
    old_publication_year, old_description = book.publication_year, book.description

    book_repo.update_book_data(book_id=book.id, new_data=update_book.model_dump(exclude_unset=True))

    updated_book = book_repo.get_book_by_id(book_id=mock_books[0].id)

    assert book.id == updated_book.id
    assert old_publication_year != updated_book.publication_year
    assert old_description != updated_book.description



