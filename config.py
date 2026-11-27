"""Environment-backed application settings."""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    discord_bot_token: str = Field(default="", repr=False)
    discord_guild_id: int | None = None
    submission_channel_id: int | None = None
    approval_channel_id: int | None = None
    admin_user_ids: str = ""
    allowed_submitter_ids: str = ""
    telegram_bot_token: str = Field(default="", repr=False)
    telegram_admin_user_ids: str = ""
    telegram_allowed_submitter_ids: str = ""
    binance_square_openapi_key: str = Field(default="", repr=False)
    cryptowire_secret_key: str = Field(default="", repr=False)
    binance_square_secret_file: str = "storage/binance_square_api_key.enc"
    database_url: str = "sqlite:///cryptowire.db"
    log_level: str = "INFO"

    @field_validator("discord_guild_id", "submission_channel_id", "approval_channel_id")
    @classmethod
    def validate_optional_discord_ids(cls, value: int | None) -> int | None:
        if value is not None and value <= 0:
            raise ValueError("Discord IDs must be positive integers")
        return value

    @staticmethod
    def _parse_ids(value: str) -> set[int]:
        parsed: set[int] = set()
        for item in value.split(","):
            item = item.strip()
            if item:
                user_id = int(item)
                if user_id <= 0:
                    raise ValueError("Platform user IDs must be positive integers")
                parsed.add(user_id)
        return parsed

    @property
    def admins(self) -> set[int]:
        return self._parse_ids(self.admin_user_ids)

    @property
    def allowed_submitters(self) -> set[int]:
        return self._parse_ids(self.allowed_submitter_ids)

    @property
    def telegram_admins(self) -> set[int]:
        return self._parse_ids(self.telegram_admin_user_ids)

    @property
    def telegram_allowed_submitters(self) -> set[int]:
        return self._parse_ids(self.telegram_allowed_submitter_ids)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
