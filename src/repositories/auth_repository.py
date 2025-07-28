from typing import Tuple
from sqlalchemy import Row, select
from sqlalchemy.orm import Session

from core.models import User, db_helper
from core.schemas.users import UserLoginInfo


class AuthRepository:
    def __init__(self, session: Session):
        self._session = session

    def find_user_by_email(
        self,
        email: str,
    ) -> Row[Tuple[str]] | None:
        stmt = select(User.email).where(User.email == email)

        result = self._session.execute(stmt)

        return result.first()

    def get_data_by_email(
        self,
        username: str,
    ) -> UserLoginInfo | None:
        stmt = select(User).where(User.email == username)
        result = self._session.scalar(stmt)

        return result
