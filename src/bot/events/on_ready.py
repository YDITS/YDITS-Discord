"""

YDITS for Discord

Copyright (c) よね/Yone

Licensed under the Apache License 2.0.

"""

from __main__ import *
from bot.tasks import *


async def on_ready(self):
    print("[INFO] Logged in.")
    commands = await self.tree.sync()
    num_commands = len(commands)
    print(f"[INFO] {num_commands} command(s) has synced.")
    print("[INFO] Ready.")
    return
