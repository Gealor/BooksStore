from core.schemas.users import UserRead
from auth import tools as auth_tools
from core.config import settings

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.jwt.access_token_expire_minutes,
) -> str:
    jwt_payload = {
        TOKEN_TYPE_FIELD: token_type,
    }
    jwt_payload.update(token_data)

    token = auth_tools.encode_jwt(payload=jwt_payload, expire_minutes=expire_minutes)
    return token


def create_access_token(user: UserRead) -> str:
    jwt_payload = {
        "sub": str(user.id),
        "name": user.name,
        "email": user.email,
    }

    access_token = create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.jwt.access_token_expire_minutes,
    )
    return access_token


def create_refresh_token(user: UserRead) -> str:
    jwt_payload = {
        "sub": str(user.id),
    }

    refresh_token = create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.jwt.get_refresh_minutes_from_days(),
    )
    return refresh_token
