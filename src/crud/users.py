from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from auth import tools as auth_tools
from core.models import User, db_helper
from core.schemas.user import UserCreate, UserNameMail, UserRead, UserUpdate


async def get_all_users(
    session : AsyncSession,
) -> Sequence[UserRead]:
    stmt = select(User).order_by(User.id)

    result = await session.scalars(stmt)
    return result.all()

async def get_user_by_id(
    user_id : int,
    session : AsyncSession,
) -> UserRead | None:
    stmt = select(User).where(User.id == user_id)
    result = await session.scalar(stmt)

    return result

async def create_user(
    user_create : UserCreate,
    session : AsyncSession,
) -> UserRead:
    user_create.password = auth_tools.hash_password(user_create.password).decode('utf-8')
    
    user = User(**user_create.model_dump())
    session.add(user)
    await session.flush()
    return user

async def delete_user_by_id(
    user_id : int,
    session : AsyncSession,
) -> None:
    stmt = select(User).options(selectinload(User.borrowed_books)).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user:
        await session.delete(user)
        await session.flush()

async def update_user_data(
    user : User,
    new_data : dict,
    session : AsyncSession,
) -> None:
    if "password" in new_data:
        new_data["password"] = auth_tools.hash_password(new_data['password']).decode('utf-8')
    for key, value in new_data.items():
        setattr(user, key, value)
        
    await session.flush()