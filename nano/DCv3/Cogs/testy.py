from nano.DCv3.bot import NanoDC
from nano.DCv3 import deco
from discord import app_commands
import discord

async def setup(nano: NanoDC):
    await nano.add_cog(testy(nano))

class testy(deco.Cog):
    @app_commands.command(name="pin",description="mew better believe it's gonna be pon")
    async def pin(mew,nya: discord.Interaction):
        await nya.response.send_message(content="pon!")