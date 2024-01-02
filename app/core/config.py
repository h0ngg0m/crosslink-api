from functools import lru_cache
from os import getenv
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PACKAGE_ROOT = Path(__file__).resolve().parent.parent.parent


def get_dotenv_paths() -> list[Path]:
    dotenv_path = PACKAGE_ROOT / "dotenvs"
    env = getenv("DEPLOYMENT_ENVIRONMENT", "local")
    return [dotenv_path / f".env.{env}", dotenv_path / ".env"]


class Settings(BaseSettings):
    DEPLOYMENT_ENVIRONMENT: str
    ACCESS_TOKEN_EXPIRE_HOURS: int
    SECRET_KEY: str
    MYSQL_USERNAME: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_DB_NAME: str
    TEST_DATABASE_URL: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_CALLBACK_URL: str
    NAVER_CLIENT_ID: str
    NAVER_CLIENT_SECRET: str

    model_config = SettingsConfigDict(
        env_file=get_dotenv_paths(), env_file_encoding="utf-8", case_sensitive=True
    )


@lru_cache
def get_settings():
    return Settings()
