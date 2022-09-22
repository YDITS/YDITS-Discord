#
# main.py | YDITS for Discord
#
# (c) 2022 よね/Yone
# licensed under the Apache License 2.0
#

import os
import time

import discord
from discord.ext import commands
from dislash import InteractionClient, Option, OptionType

from data import config
from module import api


# -------------------- Init -------------------- #

os.system('cls')
print(
    f"YDITS for Discord  {config.version}\n"+\
    f"(c) 2022 よね/Yone\n\n"+\
    f"discord.py  Ver {discord.__version__}\n\n"+\
    f"--------------------\n"
)

#discord インスタンス生成
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '/', intents=intents)

#dislash インスタンス生成
slash = InteractionClient(bot)

#api
get_p2p_last = -1


# -------------------- Functions -------------------- #

# ------------------------------------------------- #
# -------------------- Discord -------------------- #
# ------------------------------------------------- #

# ---------- On ready ---------- #
@bot.event
async def on_ready():
    # await bot.change_presence(activity=discord.Game(name=""))
    print(">Ready.  Waiting for any command and message\n")


# ---------- Commands ---------- #
# ----- info ----- #
@slash.slash_command(
    name = 'info',
    description = '情報表示',
)
async def info(inter):
    embed = discord.Embed(
        title="YDITS",
        color= 0x40ff40,
        description=""
    )
    embed.add_field(
        name=f'Ver {config.version}',
        value='(c) 2022 よね/Yone\n'+
            '不具合等の連絡は <@892376684093898772> までお願いいたします。'
    )
    await inter.reply(embed=embed)
    return


# ----- eqinfo ----- #
@slash.slash_command(
    name = 'eqinfo',
    description = '最新の地震情報を表示',
)
async def eqinfo(inter):

    global get_p2p_last

    nowTime = time.time()

    #前回のコマンド実行との間隔が10秒以上の場合
    if nowTime - get_p2p_last >= 10:
        resCode, resData = await api.get_p2p()
        get_p2p_last = nowTime

    #前回のコマンド実行との間隔が10秒未満の場合
    else:
        resCode = 0x0200
        resData = None

    #エラーを定義
    errors = {
        0x0200:  "コマンドの実行頻度が多すぎます。\n"+
                 "約10秒間お待ちください。",
        0x0201:  "地震情報の取得に失敗しました。",
        0x0202:  "JSONの解析に失敗しました。",
        0x0203:  "リクエストが多すぎます。",
        0x0204: f"HTTP {resData} が発生しました。",
        0x0205:  "JSONのデータアクセスで問題が発生しました。"
    }

    #エラーの場合
    if resCode in errors:
        await inter.reply(
            embed=discord.Embed(
                title="エラーが発生しました",
                color= 0xff4040,
                description=f"{errors[resCode]}\n"
            )
            .set_footer(
                text=f"エラーコード: {hex(resCode)}"
            )
        )
        return

    #正常時
    else:

        #embed生成
        embed = discord.Embed(
            title=resData[0],
            color=resData[1],
            description=resData[2]
        )

        await inter.reply(embed=embed)


# ---------- RUN ---------- #
bot.run(config.TOKEN)  # Login
