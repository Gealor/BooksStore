from typing import Optional
from sqlalchemy import Sequence
from sqlalchemy.orm import Session

from core.models.borrowed_books import BorrowedBook

from core.schemas.exceptions import ListBooksNotFoundException, ListUsersNotFoundException, SelfDeleteException, UserNotFoundException
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

        repo.update_user_data(user_id, values_dict)

    def delete_user(
        self,
        user_id: int,
        self_id: int,
        raise_self_delete_exc: bool = False,
    ) -> UserDelete:
        if raise_self_delete_exc and self_id == user_id:
            raise SelfDeleteException

        deleted_at = UserRepository(session=self.session).delete_user_by_id(user_id)
        if deleted_at is None:
            raise UserNotFoundException

        return {
            "deleted_at": deleted_at,
        }

    def get_users(
        self,
        include_deleted: bool = False
    ) -> Sequence[UserRead] | UserRead:
        repo = UserRepository(session=self.session)

        users = repo.get_all_users(include_deleted=include_deleted) 
        if users is None:
            raise ListUsersNotFoundException
        return [UserRead.model_validate(user) for user in users]
    
    def get_user_by_id(
        self,
        id: int,
        include_deleted: bool = False
    ) -> UserRead:
        user = UserRepository(session=self.session).get_user_by_id(user_id=id, include_deleted=include_deleted)
        if user is None:
            raise UserNotFoundException
        
        return UserRead.model_validate(user)

    def create_user(self, user_create: UserCreate) -> UserRead:
        user = UserRepository(session=self.session).create_user(user_create)
        return user
