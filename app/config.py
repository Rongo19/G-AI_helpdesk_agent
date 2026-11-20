from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    app_name: str = "GoAified HR IT Helpdesk"
    app_env: str = "development"
    debug: bool = True
    database_url: str

    # Groq LLM configuration
    groq_api_key: SecretStr
    groq_model: str = "llama-3.3-70b-versatile"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()