"""Administrator-only Binance Square API-key setup command."""

from __future__ import annotations

import logging

import discord
from discord import app_commands
from discord.app_commands import CommandTree

from config import Settings
from integrations.binance_square.credentials import save_api_key

log = logging.getLogger("cryptowire.credentials")


class BinanceApiKeyModal(discord.ui.Modal, title="Configure Binance Square API key"):
    api_key = discord.ui.TextInput(
        label="Binance Square API key",
        placeholder="Paste the API key",
        required=True,
        min_length=1,
        max_length=512,
        style=discord.TextStyle.short,
    )

    def __init__(self, settings: Settings) -> None:
        super().__init__(timeout=300)
        self.settings = settings

    async def on_submit(self, interaction: discord.Interaction) -> None:
        # Re-check authorization when the modal is submitted, not just when opened.
        if interaction.user.id not in self.settings.admins:
            await interaction.response.send_message(
                "You are not authorized to configure publishing credentials.",
                ephemeral=True,
            )
            return

        try:
            save_api_key(self.settings, str(self.api_key.value))
        except RuntimeError:
            log.error(
                "Binance Square API key setup failed because encrypted secret storage "
                "is not configured or is unavailable."
            )
            await interaction.response.send_message(
                "API key was not saved. The bot's encrypted secret storage is not "
                "configured. Ask the bot operator to configure CRYPTOWIRE_SECRET_KEY.",
                ephemeral=True,
            )
            return
        except (OSError, ValueError):
            log.error("Binance Square API key could not be saved.")
            await interaction.response.send_message(
                "API key was not saved. Check the bot's encrypted storage configuration.",
                ephemeral=True,
            )
            return

        # Never echo, log, or include the submitted credential in a response.
        await interaction.response.send_message(
            "Binance Square API key configured and encrypted successfully.",
            ephemeral=True,
        )
        log.info("Binance Square API key was configured by administrator ID %s", interaction.user.id)


def register_set_api_key_command(tree: CommandTree, settings: Settings) -> None:
    @tree.command(
        name="set_api_key",
        description="Securely configure the Binance Square publishing API key (admins only)",
    )
    async def set_api_key_command(interaction: discord.Interaction) -> None:
        if interaction.user.id not in settings.admins:
            await interaction.response.send_message(
                "Only configured CryptoWire administrators can use this command.",
                ephemeral=True,
            )
            return

        await interaction.response.send_modal(BinanceApiKeyModal(settings))
