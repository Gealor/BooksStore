from typing import Protocol, Sequence
from sqlalchemy import select
from sqlalchemy.orm import selectinload, Session

from auth import tools as auth_tools
from core.models import User
from core.schemas.users import UserCreate


class UserRepositoryAbstract(Protocol):
    def get_all_users(self) -> Sequence[User]:
        pass

    def get_user_by_id(
        self,
        user_id: int,
    ) -> User | None:
        pass

    def create_user(
        self,
        user_create: UserCreate,
    ) -> User:
        pass

    def delete_user_by_id(
        self,
        user_id: int,
    ) -> int | None:
        pass

    def update_user_data(
        self,
        user: User,
        new_data: dict,
    ) -> None:
        pass


class UserRepository(UserRepositoryAbstract):
    def __init__(self, session: Session):
        self._session = session

    def get_all_users(self) -> Sequence[User]:
        stmt = select(User).order_by(User.id)
        result = self._session.scalars(stmt)
        return result.all()

    def get_user_by_id(
        self,
        user_id: int,
    ) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = self._session.scalar(stmt)

        return result

    def create_user(
        self,
        user_create: UserCreate,
    ) -> User:
        user_create.password = auth_tools.hash_password(user_create.password).decode(
            "utf-8"
        )

        user = User(**user_create.model_dump())
        self._session.add(user)
        self._session.commit()
        return user

    def delete_user_by_id(
        self,
        user_id: int,
    ) -> int | None:
        stmt = (
            select(User)
            .options(selectinload(User.borrowed_books))
            .where(User.id == user_id)
        )
        result = self._session.execute(stmt)
        user = result.scalar_one_or_none()
        if user:
            self._session.delete(user)
            self._session.commit()
        return user.id if user else None

    def update_user_data(
        self,
        user: User,
        new_data: dict,
    ) -> None:
        if "password" in new_data:
            new_data["password"] = auth_tools.hash_password(
                new_data["password"]
            ).decode("utf-8")
        for key, value in new_data.items():
            setattr(user, key, value)

        self._session.commit()
