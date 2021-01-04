from discord.ext import commands
from discord import Colour, Embed
from .modules.amazon import amazon_search
from .modules.covid import covid_data
import duckpy


class Web(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="amazon")
    async def amazon(self, ctx, *search_term):
        search_term = " ".join(search_term)
        results = await amazon_search(search_term)

        names = results[0][0:5]
        prices = results[1][0:5]

        output = ""
        for name, price in zip(names, prices):
            output += f"""```diff
    {name}\n+{price} INR\n
    ```"""

        await ctx.send(output)

    @commands.command(name="ddg", aliases=["google"])
    async def ddg(self, ctx, *search_term):
        duck_client = duckpy.AsyncClient()
        search_term = " ".join(search_term)

        results = await duck_client.search(search_term)
        results = results[0].get("description")

        await ctx.send(results)

    @commands.command(name="covid")
    async def covid(self, ctx):
        added, total = await covid_data()

        embed = Embed(colour=Colour.blue(), title="Covid-19 [India]")
        icon = "https://i.ibb.co/CVJW8B9/62393982.jpg"
        embed.set_thumbnail(url=icon)

        fields = ["confirmed", "deceased", "recovered"]
        for field in fields:
            string = f"{total[field]} (+{added[field]})"
            embed.add_field(name=field.title(), value=string)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Web(bot))
