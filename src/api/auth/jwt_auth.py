from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.auth.tools.tools_auth import get_current_active_auth_user, validate_auth_user
from core.models import db_helper
from core.schemas.auth_info import TokenInfo
from core.schemas.user import UserBase, UserCreate, UserRead
from crud import users as users_crud
from auth import tools as auth_tools
from core.config import settings


router = APIRouter(
    prefix = settings.api.auth.prefix,
    tags = ["JWT"]
    )

@router.post('/register')
def create_user(
    user_create : UserCreate,
    session : Annotated[Session, Depends(db_helper.session_getter)]
) -> UserRead:
    user = users_crud.create_user(user_create, session)
    return user

@router.post('/login')
def auth_user_jwt(
    user : UserRead = Depends(validate_auth_user)
) -> TokenInfo:
    jwt_payload = {
        "sub" : str(user.id),
        "name" : user.name,
        "email" : user.email,
    }
    access_token = auth_tools.encode_jwt(payload = jwt_payload)
    return TokenInfo(
        access_token = access_token,
        token_type = "Bearer",
    )


