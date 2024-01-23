"""

YDITS for Discord

Copyright (c) よね/Yone

Licensed under the Apache License 2.0.

"""

import discord
import errors
from module import api


async def tsunami_info(*, self, inter: discord.Interaction):
    try:
        await inter.response.send_message("取得中", delete_after=3.0)
        tnminfoData = await api.get_tnmInfo()

        if tnminfoData["status"] == 0x0101:
            embed = discord.Embed(
                title=tnminfoData["data"]["title"],
                color=tnminfoData["data"]["color"],
                description=tnminfoData["data"]["content"],
            )
            await inter.channel.send(embed=embed)

            return

        else:
            await inter.channel.send(
                embed=discord.Embed(
                    title="エラーが発生しました",
                    color=0xFF4040,
                    description=f"{errors[tnminfoData['status']]}",
                ).set_footer(text=f"エラーコード: {hex(tnminfoData['status'])}")
            )

            return
        
    except Exception as error:
        await inter.channel.send(
            embed=discord.Embed(
                title="エラーが発生しました",
                color=0xFF4040,
                description=f"ハンドルされない例外が発生しました。```{error}```",
            ).set_footer(text=f"エラーコード: {None}")
        )

        return