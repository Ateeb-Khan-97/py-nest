from pydantic_settings import BaseSettings
from pydantic import Field


class EnvConfig(BaseSettings):
    APP_ENV: str = Field(description="Environment", default="development")
    DATABASE_URL: str = Field(description="Database URL")
    JWT_ACCESS_TOKEN_SECRET: str = Field(description="JWT Access Token Secret")
    JWT_REFRESH_TOKEN_SECRET: str = Field(description="JWT Refresh Token Secret")
    JWT_RESET_PASSWORD_TOKEN_SECRET: str = Field(
        description="JWT Reset Password Token Secret"
    )
    JWT_ACCESS_TOKEN_EXPIRY_MINUTES: int = Field(
        description="JWT Access Token Expiry in Minutes", default=15
    )
    JWT_REFRESH_TOKEN_EXPIRY_MINUTES: int = Field(
        description="JWT Refresh Token Expiry in Minutes", default=7 * 24 * 60
    )
    JWT_RESET_PASSWORD_TOKEN_EXPIRY_MINUTES: int = Field(
        description="JWT Reset Password Token Expiry in Minutes", default=5
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
        case_sensitive = True


env = EnvConfig()
is_development = env.APP_ENV == "development"
is_production = env.APP_ENV == "production"
is_testing = env.APP_ENV == "testing"
