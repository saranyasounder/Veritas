from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openrouter_api_key: str
    database_url: str
    redis_url: str
    tavily_api_key: str

    class Config:
        env_file = ".env"  # tells pydantic to load from .env file

settings = Settings()  # creates one instance, loads and validates everything