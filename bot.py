"""CryptoWire multi-platform bot entry point."""

from __future__ import annotations

import asyncio
import logging
import sys

import discord
from telegram.error import InvalidToken

from bot.client import CryptoWireClient
from bot.telegram import build_telegram_application
from config import get_settings


async def run_bots() -> None:
    settings = get_settings()
    log = logging.getLogger("cryptowire")

    missing: list[str] = []
    if not settings.discord_bot_token.strip():
        missing.append("DISCORD_BOT_TOKEN")
    if not settings.submission_channel_id:
        missing.append("SUBMISSION_CHANNEL_ID")
    try:
        if not settings.admins:
            missing.append("ADMIN_USER_IDS (at least one Discord user ID)")
        settings.allowed_submitters
        if settings.telegram_bot_token.strip() and not settings.telegram_admins:
            missing.append("TELEGRAM_ADMIN_USER_IDS (required when Telegram is enabled)")
        settings.telegram_allowed_submitters
    except ValueError:
        log.error("User ID lists must contain comma-separated positive numeric IDs")
        raise SystemExit(2)

    if missing:
        log.error("Missing required configuration: %s", ", ".join(missing))
        log.error("Copy .env.example to .env and configure the required values.")
        raise SystemExit(2)

    discord_client = CryptoWireClient(settings)
    telegram_app = None
    try:
        if settings.telegram_bot_token.strip():
            telegram_app = build_telegram_application(settings)
            await telegram_app.initialize()
            await telegram_app.start()
            if telegram_app.updater is None:
                raise RuntimeError("Telegram polling updater is unavailable")
            await telegram_app.updater.start_polling()
            log.info("Telegram submission interface started")

        await discord_client.start(settings.discord_bot_token)
    finally:
        if telegram_app is not None:
            if telegram_app.updater is not None and telegram_app.updater.running:
                await telegram_app.updater.stop()
            if telegram_app.running:
                await telegram_app.stop()
            await telegram_app.shutdown()
        if not discord_client.is_closed():
            await discord_client.close()


def main() -> None:
    settings = get_settings()
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    try:
        asyncio.run(run_bots())
    except discord.LoginFailure:
        logging.getLogger("cryptowire").error(
            "Discord rejected the bot token. Verify DISCORD_BOT_TOKEN."
        )
        sys.exit(1)
    except InvalidToken:
        logging.getLogger("cryptowire").error(
            "Telegram rejected the bot token. Verify TELEGRAM_BOT_TOKEN."
        )
        sys.exit(1)
    except KeyboardInterrupt:
        logging.getLogger("cryptowire").info("Shutdown requested")


if __name__ == "__main__":
    main()
