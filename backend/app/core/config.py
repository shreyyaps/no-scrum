from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "no-scrum-backend"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/app"


settings = Settings()
