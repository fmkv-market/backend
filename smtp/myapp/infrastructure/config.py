from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"] = "DEV"

    SMTP_HOST: str = "maildev"
    SMTP_PORT: int = 1025
    SMTP_SENDER: str = "root@localhost"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
