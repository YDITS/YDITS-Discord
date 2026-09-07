"""

YDITS for Discord

Copyright (C) 2022-2026 よね/Yone
Licensed under the Apache License 2.0.

https://github.com/YDITS/YDITS-Discord

"""

from discord.ext import commands
from ydits_discord.bot import events
from ydits_discord.bot.commands import YditsDiscordCommands
from ydits_discord.bot.tasks import YditsDiscordTasks


class YditsDiscordClient(commands.Bot):
    async def on_ready(self):
        cog = YditsDiscordCommands(client=self)
        await self.add_cog(cog)
        cog = YditsDiscordTasks(bot=self)
        await self.add_cog(cog)
        await events.on_ready(self)
