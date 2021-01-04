from discord.ext import commands
from discord.utils import get
import aiohttp


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add_emote")
    @commands.has_permissions(manage_emojis=True)
    async def add_emote(self, ctx, emote, name):
        if not emote.startswith("http"):
            try:
                emote_url = emote.split(":")[2][:-1]
            except IndexError:
                if len(emote) == 18:
                    emote_url = emote

            emote_url = f"https://cdn.discordapp.com/emojis/{emote_url}"
        else:
            emote_url = emote

        async with aiohttp.ClientSession() as session:
            async with session.get(emote_url) as resp:
                emote = await resp.read()

        await ctx.guild.create_custom_emoji(name=name, image=emote)

        emote = get(ctx.guild.emojis, name=name)
        emote = str(emote)

        await ctx.send(f"Added emote {emote}")

    @commands.command(name="del_emote")
    @commands.has_permissions(manage_emojis=True)
    async def del_emote(self, ctx, emote):
        try:
            emote = emote.split(":")[1]
        except IndexError:
            emote = emote

        emote = get(ctx.guild.emojis, name=emote)
        await emote.delete()


def setup(bot):
    bot.add_cog(Admin(bot))
