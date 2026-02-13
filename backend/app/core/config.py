"""Application configuration settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "tarot-backend"
    app_version: str = "0.1.0"
    app_env: str = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/tarot_db"
    database_pool_size: int = 20
    database_max_overflow: int = 10

    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_pool_size: int = 10

    # JWT
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    # Password
    bcrypt_rounds: int = 12

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # DeepSeek
    deepseek_api_key: str = ""
    deepseek_model: str = "deepseek/deepseek-chat"

    # Anthropic
    anthropic_api_key: str = ""

    # Stripe
    stripe_api_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_publishable_key: str = ""

    # Frontend
    frontend_url: str = "http://localhost:3000"

    # Email (Resend)
    resend_api_key: str = ""
    resend_from_email: str = "noreply@tarot.com"

    # SMS (Twilio)
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_phone_number: str = ""

    # Quota settings
    anonymous_free_quota: int = 3
    anonymous_quota_days: int = 7
    user_free_quota_weekly: int = 3
    subscription_daily_limit: int = 200
    subscription_weekly_limit: int = 700

    # Reading retention
    reading_retention_days: int = 180


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
