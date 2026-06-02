from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/.env — resolved relative to this file (backend/app/core/config.py) so it
# loads regardless of the working directory the process is launched from, e.g.
# `cd backend/app && uv run fastapi dev`. In Docker this file is ignored anyway:
# compose sets DATABASE_URL as a real env var, which takes precedence over .env.
ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")

    app_name: str = "no-scrum-backend"
    database_url: str  = Field(default="...")


settings = Settings()
