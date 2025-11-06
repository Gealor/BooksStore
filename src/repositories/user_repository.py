from datetime import datetime
from typing import Sequence
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload, Session
from sqlalchemy.exc import IntegrityError


from auth import hash_password
from core.models import User
from core.logger import log
from core.schemas.users import UserCreate


class UserRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_all_users(self, include_deleted: bool = False) -> Sequence[User]:
        stmt = select(User).order_by(User.id)
        if not include_deleted:
            stmt = stmt.where(User.deleted_at.is_(None))
        result = self._session.scalars(stmt)
        return result.all()

    def get_user_by_id(
        self,
        user_id: int,
        include_deleted: bool = False,
    ) -> User | None:
        stmt = select(User).where(User.id == user_id)
        if not include_deleted:
            stmt = stmt.where(User.deleted_at.is_(None))
        result = self._session.scalar(stmt)

        return result

    def create_user(
        self,
        user_create: UserCreate,
    ) -> User:
        user_create.password = hash_password(user_create.password).decode("utf-8")
        try:
            user = User(**user_create.model_dump())
            self._session.add(user)
        except IntegrityError as e:
            log.error("Database Exception: %s", e)
            self._session.rollback()
        else:
            self._session.commit()
        return user

    def delete_user_by_id(
        self,
        user_id: int,
    ) -> datetime | None:
        stmt = update(User).values(deleted_at=datetime.now()).where(User.id == user_id).returning(User.deleted_at)
        try:
            result = self._session.execute(stmt)
            deleted_at = result.scalar_one_or_none()
        except IntegrityError as e:
            log.error("Database Exception: %s", e)
            self._session.rollback()
        self._session.commit()
        return deleted_at

    def update_user_data(
        self,
        user_id: int,
        new_data: dict,
    ) -> None:
        if "password" in new_data:
            new_data["password"] = hash_password(new_data["password"]).decode("utf-8")
        try:
            stmt = update(User).values(**new_data).where(User.id == user_id)
            self._session.execute(stmt)
        except IntegrityError as e:
            log.error("Database Exception: %s", e)
            self._session.rollback()
        self._session.commit()