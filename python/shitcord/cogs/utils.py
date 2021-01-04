from discord.ext import commands
from discord.utils import get
from discord import Colour, Embed, Member


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="doas")
    async def doas(self, ctx, member: Member, *args):
        name = member.display_name
        avatar = member.avatar_url
        message = " ".join(args)
        hook_name = "doas"
        hooks = await ctx.channel.webhooks()
        hook = get(hooks, name=hook_name)
        if hook is None:
            hook = await ctx.channel.create_webhook(name=hook_name)
        await hook.send(content=message, username=name, avatar_url=avatar)
        await ctx.message.delete()

    @commands.command(name="poll")
    async def poll(self, ctx, title, *args):
        count = 0
        values = []
        numbers = [
            "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"
        ]

        for number, choice in zip(numbers, args):
            string = f"{number} {choice}"
            values.append(string)
            count += 1

        embed = Embed(
            colour=Colour.blue(), title=title, description="\n".join(values)
        )
        embed.set_footer(text=f"By {ctx.author.name}")

        if count > 1:
            message = await ctx.send(embed=embed)
            count_ = 0
            for reaction in numbers:
                count_ += 1
                if count_ <= count:
                    await message.add_reaction(reaction)
        else:
            message = await ctx.send(
                "Must provide atleast 2 choices for poll!"
            )

    @commands.command(name="whois")
    async def whois(self, ctx, member: Member = None):
        if not member:
            member = ctx.message.author

        embed = Embed(colour=Colour.blue(), title=f"whois {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Name", value=member.display_name)
        embed.add_field(name="Created Account On",
                        value=member.created_at.strftime("%a, %#d %B %Y"))
        embed.add_field(name="Joined Server On",
                        value=member.joined_at.strftime("%a, %#d %B %Y"))

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utils(bot))
