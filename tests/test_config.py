import pytest
from pydantic import ValidationError

from config import Settings


@pytest.mark.parametrize("field", ["discord_guild_id", "submission_channel_id", "approval_channel_id"])
@pytest.mark.parametrize("value", [0, -1])
def test_discord_snowflake_ids_must_be_positive(field: str, value: int) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: value})


def test_platform_user_id_lists_are_parsed_separately() -> None:
    settings = Settings(
        admin_user_ids="101, 102",
        allowed_submitter_ids="103",
        telegram_admin_user_ids="201",
        telegram_allowed_submitter_ids="202,203",
    )
    assert settings.admins == {101, 102}
    assert settings.allowed_submitters == {103}
    assert settings.telegram_admins == {201}
    assert settings.telegram_allowed_submitters == {202, 203}


def test_telegram_bot_token_is_optional_for_discord_only_deployments() -> None:
    settings = Settings(discord_bot_token="discord-token")
    assert settings.telegram_bot_token == ""
