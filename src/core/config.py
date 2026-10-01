from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GEMINI_API_KEY: str

    MODEL_NAME: str = "gemini-3.1-flash-lite"
    LANGUAGE: str = "pt-BR"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()