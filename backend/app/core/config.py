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