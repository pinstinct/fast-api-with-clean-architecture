from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    database_username: str
    database_password: str
    jwt_secret: str


@lru_cache  # 이미 값이 있다면 그 값을 반환
def get_settings():
    return Settings()  # 객체 생성
