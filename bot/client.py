"""CryptoWire Discord client and event handling."""

from __future__ import annotations

import logging

import discord
from discord import app_commands

from commands.help import register_help_command
from commands.set_api_key import register_set_api_key_command
from commands.status import register_status_command
from config import Settings
from services.submissions import Submission, process_submission

log = logging.getLogger("cryptowire.discord")


class CryptoWireClient(discord.Client):
    def __init__(self, settings: Settings) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.settings = settings
        self.tree = app_commands.CommandTree(self)

        register_help_command(self.tree)
        register_status_command(self.tree, settings)
        register_set_api_key_command(self.tree, settings)

    async def setup_hook(self) -> None:
        if self.settings.discord_guild_id:
            guild = discord.Object(id=self.settings.discord_guild_id)
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            log.info("Synced %d application commands to guild %s", len(synced), guild.id)
        else:
            synced = await self.tree.sync()
            log.info("Synced %d global application commands", len(synced))

    async def on_ready(self) -> None:
        if self.user:
            log.info("Logged in as %s (ID: %s)", self.user, self.user.id)
        log.info("Submission channel configured: %s", self.settings.submission_channel_id)

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        if not self.settings.submission_channel_id:
            return
        if message.channel.id != self.settings.submission_channel_id:
            return

        accepted = process_submission(
            Submission(
                platform="discord",
                user_id=message.author.id,
                submission_id=str(message.id),
                content=message.content,
                attachment_count=len(message.attachments),
            ),
            admins=self.settings.admins,
            allowed_submitters=self.settings.allowed_submitters,
        )
        if not accepted:
            try:
                await message.reply(
                    "You are not authorized to submit content to CryptoWire.",
                    mention_author=False,
                    delete_after=12,
                )
            except discord.HTTPException:
                log.exception("Could not notify unauthorized submitter")
            return

        try:
            await message.add_reaction("📥")
        except discord.HTTPException:
            log.exception("Could not acknowledge submission message %s", message.id)

    async def close(self) -> None:
        log.info("Shutting down CryptoWire Discord client")
        await super().close()
