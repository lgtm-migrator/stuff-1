from .modules.discord_emote import emote_convert, fallback_emote
from discord.ext import commands
from discord import Member
import random
import json


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("copypasta.txt", "r") as f:
            self.copypasta_dict = json.loads(f.read())

    @commands.command(name="ban")
    async def ban(self, ctx, member: Member = None, *args):
        reason = ":/"
        if len(args) > 0:
            reason = " ".join(args)
        if not member:
            await ctx.send("Mention someone to ban!")
        elif member == ctx.message.author:
            await ctx.send("You can't ban yourself!")
        else:
            await ctx.send(f"{member} has been banned\nReason: {reason}")

    @commands.command(name="choose")
    async def choose(self, ctx, *args):
        await ctx.send(random.choice(args))

    @commands.command(name="copypasta")
    async def copypasta(self, ctx, category=None):
        output = ""

        if not category:
            copypasta_list = list(self.copypasta_dict.values())
            output = random.choice(copypasta_list)
        elif "list" in category.lower():
            output += "```\n"
            keys = self.copypasta_dict.keys()
            for key in keys:
                output += f"{key}\n"
            output += "```"
        else:
            output = self.copypasta_dict.get(category)

        if output:
            await ctx.send(output)

    @commands.command(name="emote")
    async def emote(self, ctx, *args):
        args = " ".join(args)
        await ctx.send(emote_convert(args, message=True))

    @commands.command(name="react")
    async def react(self, ctx, count, *args):
        count = int(count) + 1
        args = "".join(args).lower()
        used_emotes = []
        emotes = emote_convert(args)

        async for message in ctx.channel.history(limit=count):
            message = message

        for emote in emotes:
            if emote in used_emotes:
                emote = fallback_emote(emote)
            await message.add_reaction(emote[1])
            used_emotes.append(emote)


def setup(bot):
    bot.add_cog(Fun(bot))
