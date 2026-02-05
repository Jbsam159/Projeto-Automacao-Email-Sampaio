'''
from dotenv import load_dotenv
import os

load_dotenv()

MAX_FILE_SIZE_MB = 5
ALLOWED_CONTENT_TYPES = ["application/pdf"]
UPLOAD_DIR = "uploads"

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")
'''

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 🌍 App
    port: int = 8000

    # 🗄️ Database
    database_url: str

    # URL do Frontend
    frontend_url: str

    # URL do domínio
    frontend_dominio: str

    # ✉️ Resend
    resend_api_key: str
    email_from: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",  # 🔒 Mantém o projeto seguro
    )


settings = Settings()