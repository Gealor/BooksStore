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
    def __init__(self, session: Session):
        self.session = session

    def get_my_active_books(self, user_id: int) -> Sequence[BorrowedBook]:
        result = BorrowedBookRepository(
            session=self.session
        ).get_active_borrowed_books_by_user_id(user_id)
        if not result:
            raise ListBooksNotFoundException

        return result

    def get_history_books(
        self,
        user_id: int,
    ) -> Sequence[BorrowedBook]:
        result = BorrowedBookRepository(
            session=self.session
        ).get_history_about_books_by_user_id(user_id)

        if not result:
            raise ListBooksNotFoundException
        return result

    def update_user(
        self,
        new_data: UserUpdate,
        user_id: int,
    ) -> None:
        repo = UserRepository(session=self.session)

        found_user = repo.get_user_by_id(user_id)
        if not found_user:
            raise UserNotFoundException

        values_dict = new_data.model_dump(exclude_unset=True)

        repo.update_user_data(found_user, values_dict)

    def delete_user(
        self,
        user_id: int,
        self_id: int,
        raise_self_delete_exc: bool = False,
    ) -> UserDelete:
        if raise_self_delete_exc and self_id == user_id:
            raise SelfDeleteException

        deleted_id = UserRepository(session=self.session).delete_user_by_id(user_id)
        if deleted_id is None:
            raise UserNotFoundException

        return {
            "deleted": deleted_id,
        }

    def get_users(
        self,
        id: Optional[int],
    ) -> list[UserRead] | UserRead:
        repo = UserRepository(session=self.session)

        users = repo.get_all_users() if id is None else repo.get_user_by_id(id)
        if users is None:
            raise ListUsersNotFoundException

        return users

    def create_user(self, user_create: UserCreate) -> UserRead:
        user = UserRepository(session=self.session).create_user(user_create)
        return user
