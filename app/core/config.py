import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"
        )
    )


config = Config()
