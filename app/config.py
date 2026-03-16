from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    database_url: str
    better_auth_secret: str
    frontend_url: str = "http://localhost:3000"
    cors_origins: str = "http://localhost:3000"
    environment: str = "development"  # development or production

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS_ORIGINS string into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment.lower() == "production"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
