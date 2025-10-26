import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    REDIS_DATABASE_URL: str
    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str
    SENTRY_DSN: str = (
        "https://2a6b9a708b53b15df09d9d271eda46d2@sentry.hamravesh.com/9230"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"
        ),
        env_file_encoding="utf-8",
    )


settings = Config()
