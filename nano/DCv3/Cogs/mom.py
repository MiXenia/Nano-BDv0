from discord.ext import commands
from nano.DCv3 import deco


async def setup(nano):
    await nano.add_cog(mom(nano))

class mom(deco.Cog):
    @commands.command(name="sync")
    @commands.is_owner()
    @commands.guild_only()
    async def sync(mew, nya: commands.Context, area: str = "guild"):
        tree = mew.nano.tree
        match area:
            case "guild":
                if nya.guild is None:
                    return await nya.send("This isn't a guild!")
                else:
                    tree.copy_global_to(guild=nya.guild)
                    syncnum = await tree.sync(guild=nya.guild)
            case "global":
                syncnum = await tree.sync()
            case "clear":
                if nya.guild is None:
                    return await nya.send("This isn't a guild!")
                else:
                    tree.clear_commands(guild=nya.guild)
                    syncnum = await tree.sync(guild=nya.guild)
            case _:
                return await nya.send("that's not valid! Mew can choose from `guild`, `global`, or `clear`~!")
        await nya.send(f"Synced {len(syncnum)} command(s) in {area}!!")