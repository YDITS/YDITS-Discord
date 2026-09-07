"""

YDITS for Discord

Copyright (C) 2022-2026 よね/Yone
Licensed under the Apache License 2.0.

https://github.com/YDITS/YDITS-Discord

"""

from __main__ import *
# from ydits_discord.bot.tasks import *

async def on_ready(self):
    print("[INFO] Logged in.")
    commands = await self.tree.sync()
    num_commands = len(commands)
    print(f"[INFO] {num_commands} command(s) has synced.")
    print("[INFO] Ready.")
    return
