"""Entry point for the Discord bot."""

import logging
import os
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
# Optional: set GUILD_ID to sync slash commands instantly to one server (handy for development).
GUILD_ID = os.getenv("GUILD_ID")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("bot")


async def on_app_command_error(
    interaction: discord.Interaction, error: app_commands.AppCommandError
) -> None:
    """Global error handler for slash commands."""
    if isinstance(error, app_commands.MissingPermissions):
        message = "❌ You don't have the permissions to use this command."
    elif isinstance(error, app_commands.BotMissingPermissions):
        message = "❌ I don't have the permissions to do that."
    elif isinstance(error, app_commands.NoPrivateMessage):
        message = "❌ This command can only be used in a server."
    else:
        log.exception("Unhandled command error", exc_info=error)
        message = "⚠️ Something went wrong while running this command."

    if interaction.response.is_done():
        await interaction.followup.send(message, ephemeral=True)
    else:
        await interaction.response.send_message(message, ephemeral=True)


class Bot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(command_prefix=commands.when_mentioned, intents=intents)
        self.tree.on_error = on_app_command_error

    async def setup_hook(self) -> None:
        # Load every cog in the cogs/ folder (files starting with "_" are ignored).
        for file in sorted(Path(__file__).parent.joinpath("cogs").glob("[!_]*.py")):
            await self.load_extension(f"cogs.{file.stem}")
            log.info("Loaded cog: %s", file.stem)

        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            log.info("Synced slash commands to guild %s", GUILD_ID)
        else:
            await self.tree.sync()
            log.info("Synced slash commands globally (can take up to an hour to appear)")

    async def on_ready(self) -> None:
        log.info("Logged in as %s (ID: %s)", self.user, self.user.id)
        await self.change_presence(activity=discord.Game(name="/help"))


def main() -> None:
    if not TOKEN:
        raise SystemExit("DISCORD_TOKEN is missing. Copy .env.example to .env and fill it in.")
    Bot().run(TOKEN, log_handler=None)


if __name__ == "__main__":
    main()
