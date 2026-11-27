"""Telegram polling interface for CryptoWire submissions."""

from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from config import Settings
from services.submissions import Submission, process_submission

log = logging.getLogger("cryptowire.telegram")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message:
        await update.effective_message.reply_text(
            "CryptoWire is ready. Send text or supported media to submit content. "
            "Only configured users can submit; nothing is published automatically."
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message:
        await update.effective_message.reply_text(
            "CryptoWire Telegram intake\n"
            "• Send a text message, photo, video, document, audio, or voice message to submit.\n"
            "• Access is restricted to configured Telegram administrator/submitter IDs.\n"
            "• Submissions are routed to the shared intake service used by Discord.\n"
            "• Submission does not publish anything."
        )


def _attachment_count(message) -> int:
    count = len(message.photo)
    for attribute in ("document", "video", "animation", "audio", "voice", "video_note"):
        if getattr(message, attribute, None) is not None:
            count += 1
    return count


async def handle_submission(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    user = update.effective_user
    if message is None or user is None:
        return

    settings: Settings = context.application.bot_data["settings"]
    accepted = process_submission(
        Submission(
            platform="telegram",
            user_id=user.id,
            submission_id=str(message.message_id),
            content=message.text or message.caption or "",
            attachment_count=_attachment_count(message),
        ),
        admins=settings.telegram_admins,
        allowed_submitters=settings.telegram_allowed_submitters,
    )
    if not accepted:
        await message.reply_text("You are not authorized to submit content to CryptoWire.")
        return

    await message.reply_text(
        "📥 Submission received by CryptoWire. It has not been published."
    )


def build_telegram_application(settings: Settings) -> Application:
    """Build the Telegram app; caller owns initialize/start/polling/shutdown."""
    application = Application.builder().token(settings.telegram_bot_token).build()
    application.bot_data["settings"] = settings
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    supported_content = (
        filters.TEXT
        | filters.PHOTO
        | filters.VIDEO
        | filters.Document.ALL
        | filters.AUDIO
        | filters.VOICE
        | filters.ANIMATION
        | filters.VIDEO_NOTE
    )
    application.add_handler(
        MessageHandler(supported_content & ~filters.COMMAND, handle_submission)
    )
    return application
