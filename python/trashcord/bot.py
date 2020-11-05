from duckpy import AsyncClient
import discord
import logging
import random
from discord.ext import commands
from modules.covid import covid_data
from modules.amazon import amazon_search
from modules.discord_emote import emote_convert, fallback_emote
from discord.utils import get

client = commands.Bot(command_prefix="/")
logging.basicConfig(level=logging.INFO)


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    if reaction.emoji == "👎":
        if message.author == client.user:
            await message.delete()


@client.listen("on_message")
async def nitro(message):
    # Don't respond to bots/webhooks
    if message.author.bot:
        return

    content = message.content

    # Extract emotes from message
    emote_list = []
    for item in content.split():
        if item[0] == item[-1] == ":":
            emote_list.append(item[1:-1])

    # Get emote IDs from name
    content_updated = False
    for emote in emote_list:
        emote = get(client.emojis, name=emote)
        if emote is not None:
            emote = str(emote)
            replace_emote = emote.split(":")[1]
            # Replace emote name with ID
            content = content.replace(f":{replace_emote}:", emote)
            content_updated = True

    # Don't send the same message without emotes
    if not content_updated:
        return

    # Send message via webhook
    await doas(message, message.author, content)


@client.command()
async def doas(ctx, member: discord.Member, *args):
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


@client.command(aliases=["google"])
async def ddg(ctx, *search_term):
    client = AsyncClient()
    search_term = " ".join(search_term)
    results = await client.search(search_term)
    results = results[0].get("description")
    await ctx.send(results)


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
async def copypasta(ctx, category=None):
    copypasta_dict = {
        "category": "pasta"
        }

    output = ""

    if category is None:
        copypasta_list = list(copypasta_dict.values())
        output = random.choice(copypasta_list)
    elif "list" in category.lower():
        output += "```"
        keys = copypasta_dict.keys()
        for key in keys:
            output += f"{key}\n"
        output += "```"
    else:
        output = copypasta_dict.get(category)

    if output != "":
        await ctx.send(output)


@client.command()
async def react(ctx, count, *args):
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
async def ban(ctx, member: discord.Member = None, *args):
    reason = ""
    if len(args) > 0:
        reason = "for " + " ".join(args)
    if not member:
        member = ctx.message.author
    if member == ctx.message.author:
        await ctx.send("You can't ban yourself")
    else:
        await ctx.send("{} has been banned {}".format(member, reason))


@client.command()
async def unban(ctx, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    if member == ctx.message.author:
        await ctx.send("You can't unban yourself")
    else:
        await ctx.send("{} has been unbanned".format(member))


@client.command()
async def emote(ctx, *args):
    args = " ".join(args)
    await ctx.send(emote_convert(args, message=True))


@client.command()
async def choose(ctx, *args):
    await ctx.send(random.choice(args))


client.run("TOKEN")
