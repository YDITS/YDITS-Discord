"""

eqinfo.py | bot/commands | YDITS for Discord

Copyright (c) 2022-2023 よね/Yone
Licensed under the Apache License 2.0

"""

import discord

import errors
from module import api


async def eqinfo(*, self, inter: discord.Interaction):
    await inter.response.send_message("取得中", delete_after=3.0)
    eqinfoData = await api.getEqinfo()

    if eqinfoData["status"] == 0x0101:
        embed = discord.Embed(
            title=eqinfoData["data"]["title"],
            color=eqinfoData["data"]["color"],
            description=eqinfoData["data"]["content"],
        )
        await inter.channel.send(embed=embed)

        return

    else:
        await inter.channel.send(
            embed=discord.Embed(
                title="エラーが発生しました",
                color=0xFF4040,
                description=f"{errors[eqinfoData['status']]}",
            ).set_footer(text=f"エラーコード: {hex(eqinfoData['status'])}")
        )

        return
