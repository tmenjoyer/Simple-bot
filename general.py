"""General-purpose commands."""

import discord
from discord import app_commands
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description="Check the bot's latency.")
    async def ping(self, interaction: discord.Interaction) -> None:
        latency_ms = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"🏓 Pong! `{latency_ms} ms`")

    @app_commands.command(name="help", description="List the available commands.")
    async def help(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title="Available commands", color=discord.Color.blurple())
        for command in sorted(self.bot.tree.get_commands(), key=lambda c: c.name):
            embed.add_field(name=f"/{command.name}", value=command.description, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="userinfo", description="Show information about a user.")
    @app_commands.describe(user="The user to look up (defaults to you).")
    async def userinfo(
        self, interaction: discord.Interaction, user: discord.User | None = None
    ) -> None:
        user = user or interaction.user
        embed = discord.Embed(title=str(user), color=discord.Color.blurple())
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="ID", value=user.id)
        embed.add_field(name="Bot", value="Yes" if user.bot else "No")
        embed.add_field(
            name="Account created", value=discord.utils.format_dt(user.created_at, "D")
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serverinfo", description="Show information about this server.")
    @app_commands.guild_only()
    async def serverinfo(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        embed = discord.Embed(title=guild.name, color=discord.Color.blurple())
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name="Channels", value=len(guild.channels))
        embed.add_field(name="Roles", value=len(guild.roles))
        embed.add_field(name="Created", value=discord.utils.format_dt(guild.created_at, "D"))
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))
