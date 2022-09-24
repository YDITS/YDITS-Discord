#
# main.py | YDITS for Discord
#
# (c) 2022 よね/Yone
# licensed under the Apache License 2.0
#

import os
import time

#Discord Bot
import discord
from discord.ext import commands
from dislash import InteractionClient, Option, OptionType

#Config
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


# ---------- Instance ---------- #
#discord
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '/', intents=intents)

#dislash
slash = InteractionClient(bot)


# ---------- Init val---------- #
cooldownTime = 10
cmdUseLast   = -1


# -------------------- Functions -------------------- #
# ---------- On ready ---------- #
@bot.event
async def on_ready():
    print(">Ready.  Waiting for any command and message\n")


# ---------- Commands ---------- #
def chkCooldown():

    global cmdUseLast

    nowTime = time.time()

    if not(nowTime - cmdUseLast <= cooldownTime):
        cmdUseLast = nowTime
        return True, None
    else:
        return False, int(cooldownTime - (nowTime - cmdUseLast))


# ----- Too many ----- #
async def tooMany(inter, time):
    await inter.reply(
        embed=discord.Embed(
            title="エラーが発生しました",
            color= 0xff4040,
            description= "コマンドの実行頻度が多すぎます。\n"+
                        f"約{time}秒間お待ちください。"
        )
        .set_footer(
            text=f"エラーコード: 0x0201"
        )
    )
    return


# ----- info ----- #
@slash.slash_command(
    name = 'info',
    description = '情報表示',
)
async def info(inter):

    isCooldown, time = chkCooldown()

    if isCooldown:
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

    else:
        await tooMany(inter, time)
        return


# ----- eqinfo ----- #
@slash.slash_command(
    name = 'eqinfo',
    description = '最新の地震情報を表示',
)
async def eqinfo(inter):

    isCooldown, time = chkCooldown()

    print(isCooldown, time)

    #前回のコマンド実行との間隔が10秒以上の場合
    if isCooldown:

        await inter.reply("取得中", delete_after=3.0)
        resCode, resData = await api.get_p2p()

        #エラーを定義
        errors = {
            0x0301: "地震情報の取得に失敗しました。\n",
            0x0302: "JSONの解析に失敗しました。",
            0x0303: "リクエストが多すぎます。",
            0x0304: "HTTP NG が発生しました。",
            0x0305: "JSONのデータアクセスで問題が発生しました。"
        }

        #正常時
        if resCode == 0x0101:
            
            #embed生成
            embed = discord.Embed(
                title=resData[0],
                color=resData[1],
                description=resData[2]
            )

            await inter.reply(embed=embed)
            return

        #エラー時
        else:

            await inter.reply(
                embed=discord.Embed(
                    title="エラーが発生しました",
                    color= 0xff4040,
                    description=f"{errors[resCode]}```{resData}```"
                )
                .set_footer(
                    text=f"エラーコード: {hex(resCode)}"
                )
            )
            return

    #前回のコマンド実行との間隔が10秒未満の場合
    else:
        await tooMany(inter, time)
        return


# ---------- RUN ---------- #
bot.run(config.TOKEN)  # Login
