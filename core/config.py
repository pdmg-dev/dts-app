from pydantic_settings import BaseSettings
from pydantic import Field
from datetime import timedelta


class Settings(BaseSettings):
    # App Information
    app_name: str = Field("DTS App", description="Application name")
    version: str = Field("0.1.0", description="Application version")

    # Database
    db_url: str = Field("sqlite:///./dts_app.db", description="Database connection URL")

    # JWT/Auth
    jwt_secret_key: str = Field("supersecret", description="Secret key for JWT")
    jwt_algorithm: str = Field("HS256", description="Algorithm for JWT")
    access_token_expire_minutes: int = Field(30, description="JWT expiration in minutes")

    @property
    def access_token_expire_timedelta(self) -> timedelta:
        """Handy timedelta for JWT expiration."""
        return timedelta(minutes=self.access_token_expire_minutes)

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",  # ignores unknown env vars
    }


settings = Settings()