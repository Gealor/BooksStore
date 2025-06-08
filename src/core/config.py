from fastapi import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent

ENV_FILE = BASE_DIR / '.env'
ENV_TEMPLATE_FILE = BASE_DIR / '.env.template'

class RunConfig(BaseModel):
    host : str = '0.0.0.0'
    port : str = 8000

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = (ENV_TEMPLATE_FILE, ENV_FILE),
        case_sensitive = False,
        env_nested_delimiter="__",
        env_prefix='APP_CONFIG__',
    )

    run : RunConfig = RunConfig()

settings = Settings()