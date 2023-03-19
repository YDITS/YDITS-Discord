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

            for channel in config.eew_channels:
                ch = bot.get_channel(channel)
                embed = discord.Embed(
                    title=eewData['data']['title'],
                    description=eewData['data']['content'],
                    color=eewData['data']['color']
                )
                await ch.send(embed=embed)

    if eqinfoData['status'] == 0x0101:
        eqinfo_id = eqinfoData['data']['id']

        if eqinfo_id != eqinfo_id_last and eqinfo_id_last != "":
            eqinfo_id_last = eqinfo_id

            for channel in config.eqinfo_channels:
                if channel == 867692303664807946 and eqinfoData['data']['maxScale'] < 40:
                    continue

                ch = bot.get_channel(channel)
                embed = discord.Embed(
                    title=eqinfoData['data']['title'],
                    description=eqinfoData['data']['content'],
                    color=eqinfoData['data']['color']
                )
                await ch.send(embed=embed)

    return


# ---------- RUN ---------- #
bot.run(config.TOKEN)  # Login
