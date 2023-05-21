#
# bot.py | YDITS for Discord
#
# (c) 2022-2023 よね/Yone
# licensed under the Apache License 2.0
#
import os
import discord
from data import config
from module import api


# -------------------- Init -------------------- #
def clearConsole():
    return os.system('cls' if os.name in ('nt', 'dos') else 'clear')

clearConsole()

print(
    f"YDITS for Discord  Ver {config.version}\n" +
    f"(c) 2022 よね/Yone\n\n" +
    f"discord.py  Ver {discord.__version__}\n\n" +
    f"--------------------\n"
)

errors = {
    0x0301: "情報の取得がタイムアウトしました。\n",
    0x0302: "JSONの解析に失敗しました。",
    0x0303: "リクエストが多すぎます。",
    0x0304: "HTTP NG が発生しました。",
    0x0305: "JSONのデータアクセスで問題が発生しました。"
}

intents = discord.Intents.all()
intents.message_content = True
bot = discord.Client(intents=intents)
cmdTree = discord.app_commands.CommandTree(client=bot)

eew_repNum = None
eew_repNum_last = None
eqinfo_id = None
eqinfo_id_last = None


# -------------------- Functions -------------------- #
# ---------- On ready ---------- #
@bot.event
async def on_ready():
    await cmdTree.sync()
    print(">Ready.  Waiting for any command and message\n")
    return


# ---------- Commands ---------- #
@discord.app_commands.guilds(discord.Object(id=1053378444781703339))

# ----- info ----- #
@cmdTree.command(
    name='info',
    description='情報表示'
)
async def info(inter: discord.Interaction):
    embed = discord.Embed(
        title="YDITS",
        color=0x40ff40,
        description=""
    )
    embed.add_field(
        name=f'Ver {config.version}',
        value='(c) 2022-2023 よね/Yone\n' +
              '不具合等の連絡は <@892376684093898772> までお願いいたします。'
    )
    await inter.response.send_message(embed=embed)

    return


# ----- eqinfo ----- #
@cmdTree.command(
    name='eqinfo',
    description='最新の地震情報を表示'
)
async def eqinfo(inter: discord.Interaction):
    global errors

    await inter.response.send_message("取得中", delete_after=3.0)
    eqinfoData = await api.getEqinfo()

    if eqinfoData['status'] == 0x0101:
        embed = discord.Embed(
            title=eqinfoData['data']['title'],
            color=eqinfoData['data']['color'],
            description=eqinfoData['data']['content']
        )
        await inter.channel.send(embed=embed)

        return

    else:
        await inter.channel.send(
            embed=discord.Embed(
                title="エラーが発生しました",
                color=0xff4040,
                description=f"{errors[eqinfoData['status']]}"
            )
            .set_footer(
                text=f"エラーコード: {hex(eqinfoData['status'])}"
            )
        )

        return


# ----- tnmInfo ----- #
@cmdTree.command(
    name='tsunami-info',
    description='津波情報を表示'
)
async def tnmInfo(inter: discord.Interaction):
    global errors

    await inter.response.send_message("取得中", delete_after=3.0)
    tnminfoData = await api.get_tnmInfo()

    if tnminfoData['status'] == 0x0101:
        embed = discord.Embed(
            title=tnminfoData['data']['title'],
            color=tnminfoData['data']['color'],
            description=tnminfoData['data']['content']
        )
        await inter.channel.send(embed=embed)

        return

    else:
        await inter.channel.send(
            embed=discord.Embed(
                title="エラーが発生しました",
                color=0xff4040,
                description=f"{errors[tnminfoData['status']]}"
            )
            .set_footer(
                text=f"エラーコード: {hex(tnminfoData['status'])}"
            )
        )

        return


# ----- eew ----- #
@cmdTree.command(
    name='eew',
    description='緊急地震速報および強震モニタ画像を表示'
)
async def kmoniImg(inter: discord.Interaction):
    await inter.response.send_message("取得中…", delete_after=3.0)

    eewData = await api.getEew()
    eqlvData = api.get_eqlv()
    api.get_kmoni_img()
    img = discord.File("kmoni_temp_img.gif", filename="image.gif")

    if eewData['status'] == 0x0101:
        await inter.channel.send(
            embed=discord.Embed(
                title=eewData['data']['title'],
                description=eewData['data']['content'] + "\n\n" + eqlvData['data']['content'],
                color=eewData['data']['color'],
            )
            .set_footer(
                text=f"情報提供: 防災科学技術研究所, kwatch-24h.net"
            )
            .set_image(url="attachment://image.gif"),
            file=img
        )

    else:
        await inter.channel.send(
            embed=discord.Embed(
                title="エラーが発生しました",
                color=0xff4040,
                description=f"{errors[eewData['status']]}"
            )
            .set_footer(
                text=f"エラーコード: {hex(eewData['status'])}"
            )
        )

    return


# ---------- RUN ---------- #
bot.run(config.TOKEN)  # Login
