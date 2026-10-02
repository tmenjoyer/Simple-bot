"""Basic moderation commands."""

import discord
from discord import app_commands
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @staticmethod
    def _can_act_on(interaction: discord.Interaction, target: discord.Member) -> str | None:
        """Return an error message if the action isn't allowed, otherwise None."""
        if target == interaction.user:
            return "You can't do that to yourself."
        if target == interaction.guild.owner:
            return "You can't do that to the server owner."
        if (
            interaction.user != interaction.guild.owner
            and target.top_role >= interaction.user.top_role
        ):
            return "That member's role is equal to or higher than yours."
        if target.top_role >= interaction.guild.me.top_role:
            return "That member's role is equal to or higher than mine."
        return None

    @app_commands.command(name="kick", description="Kick a member from the server.")
    @app_commands.describe(member="The member to kick.", reason="Why they are being kicked.")
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.checks.bot_has_permissions(kick_members=True)
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided",
    ) -> None:
        if error := self._can_act_on(interaction, member):
            await interaction.response.send_message(f"❌ {error}", ephemeral=True)
            return
        await member.kick(reason=f"{interaction.user}: {reason}")
        await interaction.response.send_message(f"👢 Kicked **{member}** — {reason}")

    @app_commands.command(name="ban", description="Ban a member from the server.")
    @app_commands.describe(member="The member to ban.", reason="Why they are being banned.")
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided",
    ) -> None:
        if error := self._can_act_on(interaction, member):
            await interaction.response.send_message(f"❌ {error}", ephemeral=True)
            return
        await member.ban(reason=f"{interaction.user}: {reason}")
        await interaction.response.send_message(f"🔨 Banned **{member}** — {reason}")

    @app_commands.command(name="clear", description="Delete recent messages in this channel.")
    @app_commands.describe(amount="Number of messages to delete (1-100).")
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True, read_message_history=True)
    async def clear(
        self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100]
    ) -> None:
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"🧹 Deleted {len(deleted)} message(s).", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderation(bot))
