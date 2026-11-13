from discord.ext import commands
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .bot import NanoDC

class Cog(commands.Cog):
    """
    A base Cog class that will have a global error handler in the future.
    Currently just declares if a cog is online via a print statement.
    """
    def __init__(mew, nano: "NanoDC"):
        mew.nano = nano
        
    async def cog_load(mew):
        await super().cog_load()
        print(f"DECO COG ONLINE: {mew.__cog_name__}")
