from datetime import datetime, timedelta
import pytest
from core.models.borrowed_books import BorrowedBook
from core.models.exceptions.book import ListBooksNotFoundException
from core.models.exceptions.user import ListUsersNotFoundException
from repositories.user_repository import UserRepository
from services.user_service import UserService

@pytest.fixture
def mock_my_active_books():
    return [
        BorrowedBook(
            id=1,
            book_id=4,
            reader_id=5,
            return_date=None,
            borrow_date=datetime.now(),
        ),
        BorrowedBook(
            id=2,
            book_id=2,
            reader_id=5,
            return_date=None,
            borrow_date=datetime.now(),
        ),
        BorrowedBook(
            id=3,
            book_id=7,
            reader_id=5,
            return_date=None,
            borrow_date=datetime.now(),
        ),
    ]

@pytest.fixture
def mock_history_books():
    curr_date = datetime.now()
    return [
        BorrowedBook(
            id=1,
            book_id=4,
            reader_id=5,
            return_date=curr_date,
            borrow_date=curr_date - timedelta(days = 1),
        ),
        BorrowedBook(
            id=2,
            book_id=2,
            reader_id=5,
            return_date=None,
            borrow_date=curr_date,
        ),
        BorrowedBook(
            id=3,
            book_id=7,
            reader_id=5,
            return_date=None,
            borrow_date=curr_date,
        ),
    ]


@pytest.mark.parametrize("user_id", [None, 5])
def test_get_users(user_service: UserService, mock_user_repo, mock_users_list, user_id: int | None):
    mock_user_repo.get_all_users.return_value = mock_users_list
    if user_id:
        mock_user_repo.get_user_by_id.return_value = mock_users_list[user_id-1]

    result = user_service.get_users(id=user_id)
    if not user_id:
        assert len(result) == len(mock_users_list)
        mock_user_repo.get_all_users.assert_called_once()
    else:
        assert result.id == user_id
        assert result.name == mock_users_list[user_id-1].name
        assert result.email == mock_users_list[user_id-1].email
        assert result.password == mock_users_list[user_id-1].password
        mock_user_repo.get_user_by_id.assert_called_once_with(user_id)


@pytest.mark.parametrize("user_id", [None, 7])
def test_get_users_empty(user_service: UserService, mock_user_repo, user_id: int | None):
    mock_user_repo.get_all_users.return_value = None
    if user_id:
        mock_user_repo.get_user_by_id.return_value = None

    with pytest.raises(ListUsersNotFoundException):
        user_service.get_users(id=user_id)
    (
        mock_user_repo.get_all_users.assert_called_once() 
        if not user_id
        else mock_user_repo.get_user_by_id.assert_called_once_with(user_id)
    )


def test_get_my_active_books(user_service: UserService, mock_borrowed_books_repo, mock_my_active_books, user_id = 7):
    mock_borrowed_books_repo.get_active_borrowed_books_by_user_id.return_value = mock_my_active_books

    result = user_service.get_my_active_books(user_id=user_id)
    assert result is not None
    assert len(result) == len(mock_my_active_books)
    mock_borrowed_books_repo.get_active_borrowed_books_by_user_id.assert_called_once_with(user_id)


def test_get_my_active_books_empty(user_service: UserService, mock_borrowed_books_repo, user_id = 7):
    mock_borrowed_books_repo.get_active_borrowed_books_by_user_id.return_value = None

    with pytest.raises(ListBooksNotFoundException):
        user_service.get_my_active_books(user_id=user_id)

    mock_borrowed_books_repo.get_active_borrowed_books_by_user_id.assert_called_once_with(user_id)


def test_get_history_books(user_service: UserService, mock_borrowed_books_repo, mock_history_books, user_id = 7):
    mock_borrowed_books_repo.get_history_about_books_by_user_id.return_value = mock_history_books

    result = user_service.get_history_books(user_id=user_id)
    assert result is not None
    assert len(result) == len(mock_history_books)
    assert result[0].borrow_date == mock_history_books[0].borrow_date
    assert result[0].return_date == mock_history_books[0].return_date

