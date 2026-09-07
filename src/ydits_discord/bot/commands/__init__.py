"""

YDITS for Discord

Copyright (C) 2022-2026 よね/Yone
Licensed under the Apache License 2.0.

https://github.com/YDITS/YDITS-Discord

"""

import discord
from discord import app_commands
from discord.ext import commands

from ydits_discord.bot.commands.info import info
from ydits_discord.bot.commands.eew import eew
from ydits_discord.bot.commands.eqinfo import eqinfo
from ydits_discord.bot.commands.tsunami_info import tsunami_info

__all__ = [
    "info",
    "eew",
    "eqinfo",
    "tsunami_info",
]


class YditsDiscordCommands(commands.Cog):
    def __init__(self, client: discord.Client) -> None:
        client = client

    @app_commands.command(name="info", description="情報表示")
    async def info(self, inter: discord.Interaction):
        await info(self=self, inter=inter)
        return

    @app_commands.command(
        name="eew", description="緊急地震速報および強震モニタ画像を表示"
    )
    async def kmoniImg(self, inter: discord.Interaction):
        await eew(self=self, inter=inter)
        return

    @app_commands.command(name="eqinfo", description="最新の地震情報を表示")
    async def eqinfo(self, inter: discord.Interaction):
        await eqinfo(self=self, inter=inter)
        return

    @app_commands.command(name="tsunami-info", description="津波情報を表示")
    async def tnm_info(self, inter: discord.Interaction):
        await tsunami_info(self=self, inter=inter)
        return
