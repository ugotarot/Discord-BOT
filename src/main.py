from random import random
from discord.ext import commands
import discord, asyncio, random
from discord.utils import get, find

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents = intents # Set up basic permissions
)

bot.author_id = "421756275425017859"  # Change to your discord id

client = discord.Client(intents=discord.Intents.default())

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.command()
async def pong(ctx):
    await ctx.send('pong')

@bot.command()
async def name(ctx):
    await ctx.send(ctx.author.name)

@bot.command()
async def d6(ctx):
    await ctx.send(random.randint(1, 6))

@bot.event
async def on_message(message):
    if message.content == "Salut tout le monde" :
        await message.channel.send("Salut tout seul " + message.author.mention)
    await bot.process_commands(message)

@bot.command()
async def admin(ctx, nickname):
    role = get(ctx.guild.roles, name="Admin")
    user = get(ctx.guild.members, name=nickname)
    if (not user):
        await ctx.send(nickname + " doesn't exist")
        return
    if not role:
        perms = discord.Permissions(manage_channels=True, kick_members=True, ban_members=True)
        await ctx.guild.create_role(name="Admin", colour=discord.Colour(0x0062ff), permissions=perms)
        role = get(ctx.guild.roles, name="Admin")
    await user.add_roles(role)

@bot.command()
async def ban(ctx, nickname):
    user = get(ctx.guild.members, name=nickname)
    if (not user):
        await ctx.send(nickname + " doesn't exist")
        return
    await user.ban(reason = None)

@bot.command()
async def count(ctx):
    onlineCount = 0
    offlineCount = 0
    idleCount = 0
    doNotDisturbCount = 0
    for user in [x for x in ctx.guild.members if not x.bot]:

        if user.status == discord.Status.online:
            onlineCount += 1
        if user.status == discord.Status.offline:
            offlineCount += 1
        if user.status == discord.Status.idle:
            idleCount += 1
        if user.status == discord.Status.do_not_disturb:
            doNotDisturbCount += 1
    msg = ""
    if onlineCount :
        msg += "" + str(onlineCount) + " members are online\n"
    if offlineCount :
        msg += "" + str(offlineCount) + " members are off\n"
    if idleCount :
        msg += "" + str(idleCount) + " members are idle\n" 
    if doNotDisturbCount :
        msg += "" + str(doNotDisturbCount) + " members do not want to be disturbed"
    await ctx.send(msg)

@bot.command()
async def xkcd(ctx):
    embed = discord.Embed()
    embed.set_image(url="https://c.xkcd.com/random/comic/")
    await ctx.send(embed=embed) 


token = ""
bot.run(token)  # Starts the bot