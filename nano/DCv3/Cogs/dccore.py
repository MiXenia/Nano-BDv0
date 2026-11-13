from discord.ext import commands
from nano.DCv3 import deco
from discord import app_commands
import discord, calendar
from nano.models import DCv2User


async def setup(nano):
    await nano.add_cog(DCCore(nano))

class DCCore(deco.Cog):
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

    @app_commands.command(name="mydata",description="Review mewr shared info!")
    async def mydata(mew,nya: discord.Interaction):
        user = await DCv2User.objects.filter(discordid=nya.user.id).afirst()
        if user:
            outview = DataPanel(user)
            await nya.response.send_message(view=outview,ephemeral=True)
        else:
            await nya.response.send_message("Mew haven't shared mewr info yet! Mew can do that with /signup!\nThis is a temporary message and will be replaced with a something cooler later!",ephemeral=True)


class DataPanel(discord.ui.LayoutView):
    def __init__(mew, user:DCv2User, *, timeout: float | None = 300) -> None:
        mew.user = user
        super().__init__(timeout=timeout)
        outtext = f"Mew asked me to call mew {user.nickname}!!"
        if bday := user.fullbirthday:
            mon, day = bday
            outtext += f"\nMewr birthday is day #{day} of {calendar.month_name[mon]}!!"
        if loc := user.location:
            lat, lon = loc
            outtext += f"\nMew live somewhere around {lat}, {lon}!!"
        if user.has_timezone:
            outtext += f"\nAs a result, mew live in the {user.timezone} timezone!!"
        mew.add_item(
            discord.ui.Container(
                discord.ui.TextDisplay(
                    f"## {user.nickname}'s data!\n-# Mew gave me some of mewr data so I could play with mew, here's all of it!"
                ),
                discord.ui.Separator(
                    visible=True,
                    spacing=discord.SeparatorSpacing.large
                ),
                discord.ui.TextDisplay(
                    outtext
                ),
                accent_colour=0xFFAADD
            )
        )
