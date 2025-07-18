from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import selectinload, Session

from auth import tools as auth_tools
from core.models import User, db_helper
from core.schemas.users import UserCreate, UserRead


def get_all_users(
    session: Session,
) -> Sequence[User]:
    stmt = select(User).order_by(User.id)

    result = session.scalars(stmt)
    return result.all()


def get_user_by_id(
    user_id: int,
    session: Session,
) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = session.scalar(stmt)

    return result


def create_user(
    user_create: UserCreate,
    session: Session,
) -> User:
    user_create.password = auth_tools.hash_password(user_create.password).decode(
        "utf-8"
    )

    user = User(**user_create.model_dump())
    session.add(user)
    session.commit()
    return user


def delete_user_by_id(
    user_id: int,
    session: Session,
) -> int | None:
    stmt = (
        select(User)
        .options(selectinload(User.borrowed_books))
        .where(User.id == user_id)
    )
    result = session.execute(stmt)
    user = result.scalar_one_or_none()
    if user:
        session.delete(user)
        session.commit()
    return user.id if user else None


def update_user_data(
    user: User,
    new_data: dict,
    session: Session,
) -> None:
    if "password" in new_data:
        new_data["password"] = auth_tools.hash_password(new_data["password"]).decode(
            "utf-8"
        )
    for key, value in new_data.items():
        setattr(user, key, value)

    session.commit()
