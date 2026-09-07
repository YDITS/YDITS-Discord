"""

YDITS for Discord

Copyright (C) 2022-2026 よね/Yone
Licensed under the Apache License 2.0.

https://github.com/YDITS/YDITS-Discord

"""

import discord
from discord.ext import commands, tasks

from ydits_discord.bot.tasks.eq import Eq


class YditsDiscordTasks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.eq = Eq(client=self.bot)
        self.eq_task.start()

    def cog_unload(self):
        self.eq_task.cancel()

    @tasks.loop(seconds=2)
    async def eq_task(self):
        await self.eq.main()
