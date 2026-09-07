"""

YDITS for Discord

Copyright (C) 2022-2026 よね/Yone
Licensed under the Apache License 2.0.

https://github.com/YDITS/YDITS-Discord

"""

import os
import discord
import ydits_discord
from ydits_discord import config
from ydits_discord.bot.client import YditsDiscordClient

def main() -> None:
    clear_console()
    show_logo()
    intents = discord.Intents.all()
    intents.message_content = True
    bot = YditsDiscordClient(command_prefix="/", intents=intents)
    bot.run(token=config.TOKEN)

def clear_console() -> int:
    if os.name in ("nt", "dos"):
        return os.system("cls")
    else:
        return os.system("clear")

def show_logo() -> None:
    print(
        f"{ydits_discord.__title__}  Ver. {ydits_discord.__version__}\n"
        f"{ydits_discord.__copyright__}\n\n"
        f"--------------------------------\n"
    )

if __name__ == "__main__":
    main()
