from pydantic import BaseModel


class TokenInfo(BaseModel):
    access_token: str # обязательное, фиксированное имя поля для открытой документации OAuth2PasswordBearer, которая включает схему password flow
    refresh_token: str | None = None
    token_type: str = "Bearer" # обязательное, фиксированное имя поля для открытой документации OAuth2PasswordBearer, которая включает схему password flow
