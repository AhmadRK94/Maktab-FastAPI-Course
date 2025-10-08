import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"
        )
    )


config = Config()
