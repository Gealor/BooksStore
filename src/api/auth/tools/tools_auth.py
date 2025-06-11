from fastapi import Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError

from api.auth.tools.creation_tokens import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, TOKEN_TYPE_FIELD
from core.models import db_helper
from core.schemas.users import UserRead
from crud import auth as auth_crud
from crud import users as users_crud
from auth import tools as auth_tools

# чтобы в документации появилось поле для ввода токена
http_bearer = HTTPBearer(auto_error=False) # чтобы не выбрасывал ошибку автоматически

oauth2_schema = OAuth2PasswordBearer(tokenUrl = '/api/auth/login')

def validate_auth_user(
    username : str = Form(description="Enter the email you used to register."), # указывается именно username из-за особенности реализации OAuth2PasswordBearer, который использует OAuth2PasswordRequestForm в качестве зависимости,
    # внутри же OAuth2PasswordRequestForm содержит поля username и password и никаких других 
    password : str = Form(),
    session : Session = Depends(db_helper.session_getter),
):

    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid username or password",
    )

    if not (user := auth_crud.get_data_by_email(username, session)):
        raise unauthed_exc
    
    if not auth_tools.compare_hashed_passwords(
        password.encode('utf-8'),
        user.password.encode('utf-8'),
    ):
        raise unauthed_exc
    
    return user

def get_jwt_token(
    token : str = Depends(oauth2_schema),
) -> dict:
    try:
        payload = auth_tools.decode_jwt(jwt_token=token)
    except InvalidTokenError as e: # может быть такое что токен содержит меньше сегментов в payload чем расчитано
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid to decode token."
        )
    return payload


def validate_token_type(payload : dict, token_type_ : str):
    token_type : str = payload.get(TOKEN_TYPE_FIELD)
    if token_type != token_type_:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token type',
        )
    
def get_user_by_token_type(payload, session) -> UserRead:
    id : int | None = int(payload.get('sub'))
    if not (user := users_crud.get_user_by_id(id, session)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
        )
    return user

def get_current_active_auth_user(
    payload : dict = Depends(get_jwt_token),
    session : Session = Depends(db_helper.session_getter),    
    dep = Depends(http_bearer), 
) -> UserRead:
    validate_token_type(payload, ACCESS_TOKEN_TYPE)
    return get_user_by_token_type(payload, session)


def get_current_active_auth_user_for_refresh(
    payload : dict = Depends(get_jwt_token),
    session : Session = Depends(db_helper.session_getter),  
    dep = Depends(http_bearer),    
) -> UserRead:
    validate_token_type(payload, REFRESH_TOKEN_TYPE)
    return get_user_by_token_type(payload, session)