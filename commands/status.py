"""Health/status command registration."""

import discord
from discord import app_commands
from discord.app_commands import CommandTree

from config import Settings


def register_status_command(tree: CommandTree, settings: Settings) -> None:
    @tree.command(name="status", description="Check CryptoWire bot status")
    async def status_command(interaction: discord.Interaction) -> None:
        embed = discord.Embed(title="CryptoWire Status", color=discord.Color.green())
        embed.add_field(name="Discord connection", value="Online", inline=True)
        embed.add_field(name="Telegram interface", value="Enabled" if settings.telegram_bot_token.strip() else "Disabled", inline=True)
        embed.add_field(name="Submission channel", value="Configured" if settings.submission_channel_id else "Not configured", inline=True)
        embed.add_field(name="Admin access list", value="Configured" if settings.admins else "Not configured", inline=True)
        embed.add_field(name="Publishing", value="Disabled — not implemented in Stage 2", inline=False)
        embed.set_footer(text="CryptoWire · Stage 2")
        await interaction.response.send_message(embed=embed, ephemeral=True)
