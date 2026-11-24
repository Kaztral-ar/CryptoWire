"""Environment-backed application settings."""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    discord_bot_token: str = ""
    discord_guild_id: int | None = None
    submission_channel_id: int | None = None
    approval_channel_id: int | None = None
    admin_user_ids: str = ""
    allowed_submitter_ids: str = ""
    binance_square_openapi_key: str = Field(default="", repr=False)
    database_url: str = "sqlite:///cryptowire.db"
    log_level: str = "INFO"

    @staticmethod
    def _parse_ids(value: str) -> set[int]:
        parsed: set[int] = set()
        for item in value.split(","):
            item = item.strip()
            if item:
                parsed.add(int(item))
        return parsed

    @property
    def admins(self) -> set[int]:
        return self._parse_ids(self.admin_user_ids)

    @property
    def allowed_submitters(self) -> set[int]:
        return self._parse_ids(self.allowed_submitter_ids)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
