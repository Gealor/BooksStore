import logging
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent

ENV_FILE = BASE_DIR / ".env"
ENV_TEMPLATE_FILE = BASE_DIR / ".env.template"
ENV_MOCK_FILE = BASE_DIR / ".env.mock"


class LogConfig(BaseModel):
    LOG_DEFAULT_FORMAT: str = (
        "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
    )
    level: int = logging.INFO
    datefmt: str = "%Y-%m-%d %H:%M:%S"

class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: str = 8000


class AuthApiPrefixConfig(BaseModel):
    prefix: str = "/auth"


class UsersApiPrefixConfig(BaseModel):
    prefix: str = "/users"


class BooksApiPrefixConfig(BaseModel):
    prefix: str = "/books"


class BusinessApiPrefixConfig(BaseModel):
    prefix: str = "/business"


class BusinessConditionsConfig(BaseModel):
    max_active_books: int = 3


class ApiPrefixConfig(BaseModel):
    prefix: str = "/api"
    auth: AuthApiPrefixConfig = AuthApiPrefixConfig()
    users: UsersApiPrefixConfig = UsersApiPrefixConfig()
    books: BooksApiPrefixConfig = BooksApiPrefixConfig()
    business: BusinessApiPrefixConfig = BusinessApiPrefixConfig()


class AuthJWTConfig(BaseModel):
    private_key_path: Path = BASE_DIR / "auth" / "certs" / "jwt-private.pem" # для подписывания/кодирования токенов
    public_key_path: Path = BASE_DIR / "auth" / "certs" / "jwt-public.pem" # для декодирования токенов
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30

    def get_refresh_minutes_from_days(self) -> int:
        return 24 * 60 * self.refresh_token_expire_days


class ValidationConfig(BaseModel):
    min_len_password: int = 5
    max_len_password: int = 30
    min_len_name: int = 2

    min_len_title: int = 1
    len_ISBN: int = 13
    max_len_description: int = 500


class DatabaseConfig(BaseModel):
    user: str
    password: str
    host: str
    port: str
    name: str

    echo: bool
    echo_pool: bool
    pool_size: int
    max_overflow: int

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }  # чтобы имена ограничений также учитывались alembic миграциями

    def get_db_url(self):
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class DatabaseMockConfig(BaseModel):
    user: str
    password: str
    host: str
    port: str
    name: str

    echo: bool
    echo_pool: bool
    pool_size: int
    max_overflow: int

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }  # чтобы имена ограничений также учитывались alembic миграциями

    def get_db_url(self):
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(ENV_TEMPLATE_FILE, ENV_MOCK_FILE, ENV_FILE),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    log: LogConfig = LogConfig()
    run: RunConfig = RunConfig()
    db: DatabaseConfig
    db_mock: DatabaseMockConfig
    api: ApiPrefixConfig = ApiPrefixConfig()
    jwt: AuthJWTConfig = AuthJWTConfig()
    business: BusinessConditionsConfig = BusinessConditionsConfig()
    validation: ValidationConfig = (
        ValidationConfig()
    )  # вспомогательные настройки для валидации, в данном случае для валидации пароля
    

settings = Settings()
