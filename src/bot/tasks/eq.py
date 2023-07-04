"""

eq.py | bot/tasks | YDITS for Discord

Copyright (c) 2022-2023 よね/Yone
Licensed under the Apache License 2.0

"""

import discord
from data import config
from module import api


class Eq:
    def __init__(self, *, client: discord.ext.commands.Bot) -> None:
        self.client = client
        self.eew_repNum = None
        self.eew_repNum_last = None
        self.eqinfo_id = None
        self.eqinfo_id_last = None

    async def main(self):
        eewData = await api.getEew()
        eqinfoData = await api.getEqinfo()

        if eewData["status"] == 0x0101:
            self.eew_repNum = eewData["data"]["repNum"]

            if self.eew_repNum != self.eew_repNum_last and self.eew_repNum != "":
                self.eew_repNum_last = self.eew_repNum

                eqlvData = api.get_eqlv()
                api.get_kmoni_img()
                img = discord.File("kmoni_temp_img.gif", filename="image.gif")

                embed = (
                    discord.Embed(
                        title=eewData["data"]["title"],
                        description=eewData["data"]["content"],
                        color=eewData["data"]["color"],
                    )
                    .set_footer(text=f"情報提供: 防災科学技術研究所")
                    .set_image(url="attachment://image.gif")
                )

                for channel in config.eew_channels:
                    ch = self.client.get_channel(channel)
                    await ch.send(embed=embed, file=img)

        if eqinfoData["status"] == 0x0101:
            self.eqinfo_id = eqinfoData["data"]["id"]

            if self.eqinfo_id != self.eqinfo_id_last and self.eqinfo_id_last != "":
                self.eqinfo_id_last = self.eqinfo_id

                embed = discord.Embed(
                    title=eqinfoData["data"]["title"],
                    description=eqinfoData["data"]["content"],
                    color=eqinfoData["data"]["color"],
                )

                for channel in config.eqinfo_channels:
                    ch = self.client.get_channel(channel)
                    await ch.send(embed=embed)

        return
