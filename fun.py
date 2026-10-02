"""Fun commands."""

import random

import discord
from discord import app_commands
from discord.ext import commands

EIGHT_BALL_ANSWERS = [
    "It is certain.",
    "Without a doubt.",
    "Yes, definitely.",
    "Most likely.",
    "Signs point to yes.",
    "Reply hazy, try again.",
    "Ask again later.",
    "Cannot predict now.",
    "Don't count on it.",
    "My sources say no.",
    "Very doubtful.",
]


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="roll", description="Roll a die.")
    @app_commands.describe(sides="Number of sides (default 6).", count="Number of dice (default 1).")
    async def roll(
        self,
        interaction: discord.Interaction,
        sides: app_commands.Range[int, 2, 1000] = 6,
        count: app_commands.Range[int, 1, 20] = 1,
    ) -> None:
        rolls = [random.randint(1, sides) for _ in range(count)]
        await interaction.response.send_message(
            f"🎲 {count}d{sides}: {', '.join(map(str, rolls))} (total: **{sum(rolls)}**)"
        )

    @app_commands.command(name="coinflip", description="Flip a coin.")
    async def coinflip(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(f"🪙 {random.choice(['Heads', 'Tails'])}!")

    @app_commands.command(name="8ball", description="Ask the magic 8-ball a question.")
    @app_commands.describe(question="Your yes/no question.")
    async def eight_ball(self, interaction: discord.Interaction, question: str) -> None:
        await interaction.response.send_message(
            f"🎱 **{question}**\n{random.choice(EIGHT_BALL_ANSWERS)}"
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))
