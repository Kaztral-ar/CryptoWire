"""Help command registration."""

import discord
from discord import app_commands
from discord.app_commands import CommandTree


def register_help_command(tree: CommandTree) -> None:
    @tree.command(name="help", description="Show CryptoWire commands and workflow")
    async def help_command(interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title="CryptoWire Help",
            description=(
                "CryptoWire receives submissions from the configured Discord channel and optional Telegram bot. "
                "Submissions are not published automatically; administrator approval "
                "will be required before Binance Square publishing."
            ),
            color=discord.Color.blurple(),
        )
        embed.add_field(name="/status", value="Check bot health and configuration status", inline=False)
        embed.add_field(
            name="/set_api_key",
            value="Administrators: securely configure the Binance Square API key using a private modal.",
            inline=False,
        )
        embed.add_field(name="Submission channels", value="Discord: configured channel. Telegram: send a message to the configured bot. Both use the same intake service.", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)
