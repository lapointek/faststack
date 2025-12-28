from typing import List

# Advance python type handling
from pydantic_settings import BaseSettings
from pydantic import field_validator


# Inherit base settings from pydantic
class Settings(BaseSettings):
    # Load variables from .env
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    DATABASE_URL: str
    ALLOWED_ORIGINS: str = ""
    # OPENAI_API_KEY: str

    # Convert ALLOWED_ORIGINS into a list
    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> List[str]:
        # Return value separated by commas if exist otherwise return empty list
        return v.split(",") if v else []

    # Set Configuration
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Instantiate class
settings = Settings()
