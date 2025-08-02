from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from api.auth.tools import tools_auth
from api.auth.tools import creation_tokens
from core.models import db_helper
from core.schemas.auth_info import TokenInfo
from core.schemas.users import UserCreate, UserRead
from core.config import settings
from services.user_service import UserService

router = APIRouter(prefix=settings.api.auth.prefix, tags=["JWT"])


@router.post("/register")
def create_user(
    user_create: UserCreate,
    session: Annotated[Session, Depends(db_helper.session_getter)],
) -> UserRead:
    user = UserService.create_user(user_create, session)
    return user


@router.post("/login")
def auth_user_jwt(user: UserRead = Depends(tools_auth.validate_auth_user)) -> TokenInfo:
    access_token = creation_tokens.create_access_token(user)
    refresh_token = creation_tokens.create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh", response_model_exclude_none=True)
def refresh_jwt(
    user: UserRead = Depends(tools_auth.get_current_active_auth_user_for_refresh),
) -> TokenInfo:
    access_token = creation_tokens.create_access_token(user)
    return TokenInfo(
        access_token=access_token,
    )
