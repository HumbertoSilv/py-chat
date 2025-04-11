from enum import Enum

from pydantic_settings import BaseSettings as Base
from pydantic_settings import SettingsConfigDict


class EnvironmentOption(Enum):
    LOCAL = 'local'
    STAGING = 'staging'
    PRODUCTION = 'production'


class BaseSettings(Base):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )


class JWTSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRES_MINUTES: int


class PostgresSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_URL: str


class EnvironmentSettings(BaseSettings):
    ENVIRONMENT: EnvironmentOption
    LOG_LEVEL: str


class Settings(JWTSettings, PostgresSettings, EnvironmentSettings):
    pass


settings = Settings()
