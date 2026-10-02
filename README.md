# Discord Bot

A simple, modular Discord bot written in Python with [discord.py](https://github.com/Rapptz/discord.py) and slash commands.

## Features

| Command | Description |
| --- | --- |
| `/ping` | Check the bot's latency |
| `/help` | List the available commands |
| `/userinfo [user]` | Show information about a user |
| `/serverinfo` | Show information about the server |
| `/roll [sides] [count]` | Roll one or more dice |
| `/coinflip` | Flip a coin |
| `/8ball <question>` | Ask the magic 8-ball |
| `/kick <member> [reason]` | Kick a member (requires *Kick Members*) |
| `/ban <member> [reason]` | Ban a member (requires *Ban Members*) |
| `/clear <amount>` | Delete recent messages (requires *Manage Messages*) |

## Setup

### 1. Create the bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application.
2. Open the **Bot** tab, then reset/copy the **token**.
3. Open **OAuth2 → URL Generator**, select the scopes `bot` and `applications.commands`, pick the permissions you need (Kick Members, Ban Members, Manage Messages, Read Message History), and use the generated URL to invite the bot to your server.

### 2. Install

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
cd YOUR-REPO

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure

```bash
cp .env.example .env
```

Edit `.env` and set your `DISCORD_TOKEN`. Optionally set `GUILD_ID` to your test server's ID so slash commands update instantly (global commands can take up to an hour to propagate).

### 4. Run

```bash
python bot.py
```

## Project structure

```
.
├── bot.py             # Entry point
├── cogs/
│   ├── general.py     # ping, help, userinfo, serverinfo
│   ├── fun.py         # roll, coinflip, 8ball
│   └── moderation.py  # kick, ban, clear
├── requirements.txt
├── .env.example
└── LICENSE
```

## Adding a command

Create a new file in `cogs/` (for example `cogs/hello.py`) with a cog and a `setup` function. It is loaded automatically at startup.

```python
import discord
from discord import app_commands
from discord.ext import commands


class Hello(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="hello", description="Say hello.")
    async def hello(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(f"Hello, {interaction.user.mention}!")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Hello(bot))
```

## Security

**Never commit your `.env` file or share your bot token.** If it leaks, reset it immediately in the Developer Portal. `.env` is already listed in `.gitignore`.

## License

[MIT](LICENSE)
