from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "ResumeAI Analyzer"
    DEBUG: bool = False

    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "resume_analyzer"

    # Gemini API
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # File upload
    MAX_FILE_SIZE_MB: int = 5
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx", ".txt"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
