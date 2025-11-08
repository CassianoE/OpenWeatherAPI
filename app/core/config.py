from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # defaults seguros para dev; em produção, sobrescreva via env
    DATABASE_URL: str = Field(
        default="postgresql+psycopg2://postgres:postgres@db:5432/weather"
    )
    OPENWEATHER_API_KEY: str

    # pydantic-settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
