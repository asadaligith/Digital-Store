"""
Application configuration using Pydantic BaseSettings.

This module handles all environment variable validation and configuration management.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All settings are validated at startup to fail fast if configuration is invalid.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # ===== Database =====
    MONGODB_URI: str = "mongodb://admin:password123@localhost:27017/ecommerce?authSource=admin"

    # ===== JWT Configuration =====
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ===== Stripe Payment Gateway =====
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str

    # ===== SendGrid Email Service =====
    SENDGRID_API_KEY: str
    SENDGRID_FROM_EMAIL: str
    SENDGRID_FROM_NAME: str = "E-Commerce Store"

    # ===== Cloudinary (Optional) =====
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    # ===== CORS =====
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    # ===== Environment =====
    ENVIRONMENT: str = "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.ENVIRONMENT.lower() == "production"

    # ===== Rate Limiting =====
    RATE_LIMIT_AUTHENTICATED: int = 100  # requests per minute
    RATE_LIMIT_ANONYMOUS: int = 20       # requests per minute

    # ===== Security =====
    BCRYPT_ROUNDS: int = 12

    # ===== Application =====
    APP_NAME: str = "E-Commerce Store"
    APP_VERSION: str = "1.0.0"


# Global settings instance
settings = Settings()


def validate_settings() -> None:
    """
    Validate critical settings at startup.

    Raises:
        ValueError: If critical settings are missing or invalid
    """
    errors = []

    # Check JWT secrets are set and not default values
    if not settings.JWT_SECRET_KEY or len(settings.JWT_SECRET_KEY) < 32:
        errors.append(
            "JWT_SECRET_KEY must be set and at least 32 characters long"
        )

    if not settings.JWT_REFRESH_SECRET_KEY or len(settings.JWT_REFRESH_SECRET_KEY) < 32:
        errors.append(
            "JWT_REFRESH_SECRET_KEY must be set and at least 32 characters long"
        )

    # Check payment gateway keys
    if not settings.STRIPE_SECRET_KEY:
        errors.append("STRIPE_SECRET_KEY must be set")

    if not settings.STRIPE_WEBHOOK_SECRET:
        errors.append("STRIPE_WEBHOOK_SECRET must be set")

    # Check email service
    if not settings.SENDGRID_API_KEY:
        errors.append("SENDGRID_API_KEY must be set")

    if not settings.SENDGRID_FROM_EMAIL:
        errors.append("SENDGRID_FROM_EMAIL must be set")

    # Raise errors if any validation failed
    if errors:
        error_message = "\n".join([f"  - {error}" for error in errors])
        raise ValueError(
            f"Configuration validation failed:\n{error_message}\n\n"
            "Please check your .env file and ensure all required environment variables are set."
        )

    print("✅ Configuration validated successfully")
