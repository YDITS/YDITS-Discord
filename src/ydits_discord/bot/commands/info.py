"""

YDITS for Discord

Copyright (C) 2022-2026 よね/Yone
Licensed under the Apache License 2.0.

https://github.com/YDITS/YDITS-Discord

"""

import discord
from ydits_discord import config


async def info(*, self, inter: discord.Integration):
    embed = discord.Embed(title="YDITS", color=0x40FF40, description="")
    embed.add_field(
        name=f"Ver {config.__version__}",
        value=(
            f"{config.__copyright__}\n"
            "不具合等の連絡は <@892376684093898772> までお願いいたします。"
        ),
    )
    await inter.response.send_message(embed=embed)
    return
