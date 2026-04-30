from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from auth.creation_tokens import create_access_token, create_refresh_token
from auth.tools_auth import authentification_user, validate_user_for_refresh
from core.models import db_helper
from core.schemas.auth_info import TokenInfo
from core.schemas.exceptions import EmailAlreadyExistsException
from core.schemas.users import UserCreate, UserRead
from core.config import settings
from services.user_service import UserService

router = APIRouter(prefix=settings.api.auth.prefix, tags=["JWT"])


@router.post("/register")
def create_user(
    user_create: UserCreate,
    session: Annotated[Session, Depends(db_helper.session_getter)],
) -> UserRead:
    try:
        user = UserService(session=session).create_user(user_create)
    except EmailAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User with this email already exist"
        )
    return user


@router.post("/login")
def auth_user_jwt(user: UserRead = Depends(authentification_user)) -> TokenInfo:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh", response_model_exclude_none=True)
def refresh_jwt(
    user: UserRead = Depends(validate_user_for_refresh),
) -> TokenInfo:
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token,
    )
