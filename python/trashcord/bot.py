import discord
import logging
import random
from discord.ext import commands
from modules.covid import covid_data
from modules.amazon import amazon_search
from modules.duckduckgo import duck_search
from modules.discord_emote import emote_convert
client = commands.Bot(command_prefix='/')
logging.basicConfig(level=logging.INFO)


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.command()
async def whois(ctx, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    embed = discord.Embed(colour=discord.Colour.blue(),
                          title="whois {}".format(member))
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Name", value=member.display_name)
    embed.add_field(name="Created Account On",
                    value=member.created_at.strftime("%a, %#d %B %Y"))
    embed.add_field(name="Joined Server On",
                    value=member.joined_at.strftime("%a, %#d %B %Y"))
    await ctx.send(embed=embed)


@client.command()
async def amazon(ctx, *search_term):
    search_term = " ".join(search_term)
    results = await amazon_search(search_term)
    names = results[0][0:5]
    prices = results[1][0:5]
    output = ""
    for name, price in zip(names, prices):
        output += f'''```diff
{name}\n+{price} INR\n
```'''
    await ctx.send(output)


@client.command()
async def ddg(ctx, *search_term):
    search_term = " ".join(search_term)
    try:
        results = await duck_search(search_term)
        await ctx.send(results)
    except:
        await ctx.send("No results found")


@client.command()
async def covid(ctx):
    added, total = await covid_data()
    embed = discord.Embed(colour=discord.Colour.blue(),
                          title="Covid-19 [India]")
    icon = "https://i.ibb.co/CVJW8B9/62393982.jpg"
    embed.set_thumbnail(url=icon)
    fields = ["confirmed", "deceased", "recovered"]
    for field in fields:
        string = f"{total[field]} (+{added[field]})"
        embed.add_field(name=field.title(), value=string)
    await ctx.send(embed=embed)

@client.command()
async def react(ctx, count, *args):
    count = int(count) + 1
    args = " ".join(args)
    emotes = emote_convert(args).split()
    async for message in ctx.channel.history(limit=count):
        message = message
    for emote in emotes:
        await message.add_reaction(emote)

@client.command()
async def poll(ctx, title, *args):
    choices = args
    count = 0
    values = []
    numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    for number, choice in zip(numbers, choices):
        string = "{} {}".format(number, choice)
        values.append(string)
        count += 1
    embed = discord.Embed(colour=discord.Colour.blue(),
            title=title, description="\n".join(values))
    embed.set_footer(text="By {}".format(ctx.author.name))
    if count > 1:
        message = await ctx.send(embed=embed)
        count_ = 0
        for reaction in numbers:
            count_ += 1
            if count_ <= count:
                await message.add_reaction(str(reaction))
    else:
        message = await ctx.send("Must provide atleast 2 choices for poll")


@client.command()
async def ban(ctx, member : discord.Member = None):
    if not member:
        member = ctx.message.author
    if member == ctx.message.author:
        await ctx.send("You cant ban yourself")
    else:
        await ctx.send("{} has been banned".format(member))


@client.command()
async def emote(ctx, *args):
    args = " ".join(args)
    await ctx.send(emote_convert(args))


@client.command()
async def choose(ctx, *args):
    await ctx.send(random.choice(args))


client.run("TOKEN")
