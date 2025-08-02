from typing import Optional
from sqlalchemy import Sequence
from sqlalchemy.orm import Session

from core.models.borrowed_books import BorrowedBook
from core.models.exceptions.book import ListBooksNotFoundException
from core.models.exceptions.user import (
    ListUsersNotFoundException,
    SelfDeleteException,
    UserNotFoundException,
)
from core.schemas.users import UserCreate, UserDelete, UserRead, UserUpdate
from repositories.borrowed_book_repository import BorrowedBookRepository
from repositories.user_repository import UserRepository


class UserService:
    @staticmethod
    def get_my_active_books(user_id: int, session: Session) -> Sequence[BorrowedBook]:
        result = BorrowedBookRepository(
            session=session
        ).get_active_borrowed_books_by_user_id(user_id)
        if not result:
            raise ListBooksNotFoundException

        return result

    @staticmethod
    def get_history_books(
        user_id: int,
        session: Session,
    ) -> Sequence[BorrowedBook]:
        result = BorrowedBookRepository(
            session=session
        ).get_history_about_books_by_user_id(user_id)

        if not result:
            raise ListBooksNotFoundException
        return result

    @staticmethod
    def update_user(
        new_data: UserUpdate,
        user_id: int,
        session: Session,
    ) -> None:
        repo = UserRepository(session=session)

        found_user = repo.get_user_by_id(user_id, session)
        if not found_user:
            raise UserNotFoundException

        values_dict = new_data.model_dump(exclude_unset=True)

        repo.update_user_data(found_user, values_dict)

    @staticmethod
    def delete_user(
        user_id: int,
        self_id: int,
        session: Session,
        raise_self_delete_exc: bool = False,
    ) -> UserDelete:
        if raise_self_delete_exc and self_id == user_id:
            raise SelfDeleteException

        deleted_id = UserRepository(session=session).delete_user_by_id(user_id)
        if deleted_id is None:
            raise UserNotFoundException

        return {
            "deleted": deleted_id,
        }

    @staticmethod
    def get_users(
        id: Optional[int],
        session: Session,
    ) -> list[UserRead] | UserRead:
        repo = UserRepository(session=session)

        users = repo.get_all_users() if id is None else repo.get_user_by_id(id)
        if users is None:
            raise ListUsersNotFoundException

        return users

    @staticmethod
    def create_user(user_create: UserCreate, session: Session) -> UserRead:
        user = UserRepository(session=session).create_user(user_create)
        return user
