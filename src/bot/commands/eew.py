"""

eew.py | bot/commands | YDITS for Discord

Copyright (c) 2022-2023 よね/Yone
Licensed under the Apache License 2.0

"""

import discord

import errors
from module import api


async def eew(self, inter: discord.Interaction):
    try:
        await inter.response.send_message("取得中…", delete_after=3.0)

        eewData = await api.getEew()
        eqlvData = api.get_eqlv()
        api.get_kmoni_img()
        img = discord.File("kmoni_temp_img.gif", filename="image.gif")

        if eewData["status"] == 0x0101:
            await inter.channel.send(
                embed=discord.Embed(
                    title=eewData["data"]["title"],
                    description=eewData["data"]["content"]
                    + "\n\n"
                    + eqlvData["data"]["content"],
                    color=eewData["data"]["color"],
                )
                .set_footer(text=f"情報提供: 防災科学技術研究所, kwatch-24h.net")
                .set_image(url="attachment://image.gif"),
                file=img,
            )

        else:
            await inter.channel.send(
                embed=discord.Embed(
                    title="エラーが発生しました",
                    color=0xFF4040,
                    description=f"{errors[eewData['status']]}",
                ).set_footer(text=f"エラーコード: {hex(eewData['status'])}")
            )

        return

    except Exception as error:
        await inter.channel.send(
            embed=discord.Embed(
                title="エラーが発生しました",
                color=0xFF4040,
                description=f"```{error}```",
            ).set_footer(text=f"エラーコード: {None}")
        )

    return
