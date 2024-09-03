"""

YDITS for Discord

Copyright (C) よね/Yone

Licensed under the Apache License 2.0.

"""

import discord
from discord.ext import commands, tasks

from bot.tasks import eq


class YditsDiscordTasks(commands.Cog):
    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot
        self.eq = eq.Eq(client=self.bot)
        self.eq_task.start()

    def cog_unload(self):
        self.eq_task.cancel()

    @tasks.loop(seconds=2)
    async def eq_task(self):
        await self.eq.main()
