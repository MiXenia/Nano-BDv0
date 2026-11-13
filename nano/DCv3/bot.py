from discord.ext import commands
import discord, os, traceback

class NanoDC(commands.Bot):
    def __init__(mew, motd: str="Bravely Daughter!"):
        intents=discord.Intents.default()
        intents.members = True
        intents.message_content = True
        intents.voice_states = True
        super().__init__(command_prefix='+', intents=intents, help_command=None)
        mew.motd = motd

    async def setup_hook(mew):
        cog_dir = os.path.join(os.path.dirname(__file__), "Cogs")
        for filename in os.listdir(cog_dir):
            if filename.endswith(".py") and not filename.startswith("_"):
                extension_name = f"nano.DCv3.Cogs.{filename[:-3]}"
                try:
                    await mew.load_extension(extension_name)
                except Exception as e:
                    print(f"Failed to load {extension_name}: {e}\n---Traceback---")
                    traceback.print_exc()
