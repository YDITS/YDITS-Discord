"""

YDITS for Discord

Copyright (c) よね/Yone
Licensed under the Apache License 2.0.

"""

import os
import discord
from bot import *
from data import config


class YditsDiscord:
    def __init__(self) -> None:
        clear_console()
        show_logo()

        intents = discord.Intents.all()
        intents.message_content = True
        bot = client.YditsDiscordClient(command_prefix="/", intents=intents)
        bot.run(token=config.TOKEN)

        return


def clear_console() -> int:
    if os.name in ("nt", "dos"):
        return os.system("cls")
    else:
        return os.system("clear")


def show_logo() -> None:
    print(
        f"{config.__title__}  Ver {config.__version__}\n"
        f"{config.__copyright__}\n\n"
        f"--------------------\n"
    )
    return


if __name__ == "__main__":
    YditsDiscord()
