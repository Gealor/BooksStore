from fastapi import Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from api.auth.tools.creation_tokens import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    TOKEN_TYPE_FIELD,
)
from core.models import db_helper
from core.schemas.users import UserRead
from auth import tools as auth_tools
from repositories.auth_repository import AuthRepository
from services.user_service import UserService

# чтобы в документации появилось поле для ввода токена
http_bearer = HTTPBearer(auto_error=False)  # чтобы не выбрасывал ошибку автоматически

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

unauthed_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid username or password",
)


def validate_auth_user(
    username: str = Form(
        description="Enter the email you used to register."
    ),  # указывается именно username из-за особенности реализации OAuth2PasswordBearer, который использует OAuth2PasswordRequestForm в качестве зависимости,
    # внутри же OAuth2PasswordRequestForm содержит поля username и password и никаких других
    password: str = Form(),
    session: Session = Depends(db_helper.session_getter),
):
    if not (user := AuthRepository(session=session).get_data_by_email(username)):
        raise unauthed_exc

    if not auth_tools.compare_hashed_passwords(
        password.encode("utf-8"),
        user.password.encode("utf-8"),
    ):
        raise unauthed_exc

    return user


def get_jwt_token(
    token: str = Depends(oauth2_schema),
) -> dict:
    try:
        payload = auth_tools.decode_jwt(jwt_token=token)
    except (
        ExpiredSignatureError
    ) as e:  # ExpiredSignatureError наследуется от ошибки InvalidTokenError
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired."
        )
    except InvalidTokenError as e:  # может быть такое что токен содержит меньше сегментов в payload чем расчитано
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid to decode token."
        )
    return payload


def validate_token_type(payload: dict, token_type_: str):
    token_type: str = payload.get(TOKEN_TYPE_FIELD)
    if token_type != token_type_:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )


def get_user_by_token_type(payload, session) -> UserRead:
    id: int | None = int(payload.get("sub"))
    if not (user := UserService.get_users(id, session)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return user


def get_current_active_auth_user(
    payload: dict = Depends(get_jwt_token),
    session: Session = Depends(db_helper.session_getter),
    dep=Depends(http_bearer),
) -> UserRead:
    validate_token_type(payload, ACCESS_TOKEN_TYPE)
    return get_user_by_token_type(payload, session)


def get_current_active_auth_user_for_refresh(
    payload: dict = Depends(get_jwt_token),
    session: Session = Depends(db_helper.session_getter),
    dep=Depends(http_bearer),
) -> UserRead:
    validate_token_type(payload, REFRESH_TOKEN_TYPE)
    return get_user_by_token_type(payload, session)
