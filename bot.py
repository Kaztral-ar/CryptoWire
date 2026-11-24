"""CryptoWire Discord bot entry point."""

from __future__ import annotations

import logging
import sys

import discord

from bot.client import CryptoWireClient
from config import get_settings


def main() -> None:
    settings = get_settings()
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    log = logging.getLogger("cryptowire")

    missing: list[str] = []
    if not settings.discord_bot_token.strip():
        missing.append("DISCORD_BOT_TOKEN")
    if not settings.submission_channel_id:
        missing.append("SUBMISSION_CHANNEL_ID")
    try:
        if not settings.admins:
            missing.append("ADMIN_USER_IDS (at least one Discord user ID)")
    except ValueError:
        log.error("ADMIN_USER_IDS must be a comma-separated list of numeric Discord user IDs")
        sys.exit(2)

    try:
        settings.allowed_submitters
    except ValueError:
        log.error("ALLOWED_SUBMITTER_IDS must be a comma-separated list of numeric Discord user IDs")
        sys.exit(2)

    if missing:
        log.error("Missing required configuration: %s", ", ".join(missing))
        log.error("Copy .env.example to .env and configure the required values.")
        sys.exit(2)

    client = CryptoWireClient(settings)
    try:
        client.run(settings.discord_bot_token, log_handler=None)
    except discord.LoginFailure:
        log.error("Discord rejected the bot token. Verify DISCORD_BOT_TOKEN.")
        sys.exit(1)
    except KeyboardInterrupt:
        log.info("Shutdown requested")


if __name__ == "__main__":
    main()
