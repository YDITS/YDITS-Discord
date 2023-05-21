#
# eq.py | YDITS for Discord
#
# (c) 2022-2023 よね/Yone
# licensed under the Apache License 2.0
#
import os
import discord
from discord.ext import tasks
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
    eq.start()
    print(">Ready.  Waiting for any command and message\n")
    return


# ---------- Tasks ---------- #
@tasks.loop(seconds=2)
async def eq():
    global eew_repNum, eew_repNum_last
    global eqinfo_id, eqinfo_id_last

    eewData = await api.getEew()
    eqinfoData = await api.getEqinfo()

    if eewData['status'] == 0x0101:
        eew_repNum = eewData['data']['repNum']

        if eew_repNum != eew_repNum_last and eew_repNum != "":
            eew_repNum_last = eew_repNum

            eqlvData = api.get_eqlv()
            api.get_kmoni_img()
            img = discord.File("kmoni_temp_img.gif", filename="image.gif")

            embed=discord.Embed(
                title=eewData['data']['title'],
                description=eewData['data']['content'] + "\n\n" + eqlvData['data']['content'],
                color=eewData['data']['color'],
            ).set_footer(
                text=f"情報提供: 防災科学技術研究所, kwatch-24h.net"
            ).set_image(url="attachment://image.gif")

            for channel in config.eew_channels:
                ch = bot.get_channel(channel)
                await ch.send(embed=embed, file=img)

    if eqinfoData['status'] == 0x0101:
        eqinfo_id = eqinfoData['data']['id']

        if eqinfo_id != eqinfo_id_last and eqinfo_id_last != "":
            eqinfo_id_last = eqinfo_id

            embed = discord.Embed(
                title=eqinfoData['data']['title'],
                description=eqinfoData['data']['content'],
                color=eqinfoData['data']['color']
            )

            for channel in config.eqinfo_channels:
                ch = bot.get_channel(channel)
                await ch.send(embed=embed)

    return


# ---------- RUN ---------- #
bot.run(config.TOKEN)  # Login
