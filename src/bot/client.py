"""

client.py | bot | YDITS for Discord

Copyright (c) 2022-2023 よね/Yone
Licensed under the Apache License 2.0

"""

from discord.ext import commands
from bot.commands import *
from bot.events import *
from bot.tasks import *


class YditsDiscordClient(commands.Bot):
    async def on_ready(self):
        cog = YditsDiscordCommands(client=self)
        await self.add_cog(cog)
        cog = YditsDiscordTasks(bot=self)
        await self.add_cog(cog)
        await on_ready.on_ready(self)
