from typing import Tuple
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.models import User, db_helper
from core.schemas.users import UserLoginInfo


def find_user_by_email(
    email: str,
    session: Session,
) -> Tuple[str] | None:
    stmt = select(User.email).where(User.email == email)

    result = session.execute(stmt)

    return result.first()


def get_data_by_email(
    username: str,
    session: Session,
) -> UserLoginInfo | None:
    stmt = select(User).where(User.email == username)
    result = session.scalar(stmt)

    return result
