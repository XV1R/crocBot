import discord
from discord.ext import commands
from discord import Spotify
import random
import asyncio
import subprocess
import os

description = "My first bot; works as a testing ground"
#the bot instance
client = commands.Bot(command_prefix='$', description=description)



token = open('token.txt')
token = token.readlines()
print(token)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    print(client.user.name)
    print(client.user.id)
    print('------------')

@client.event
async def on_message(message):
    #makes sure the bot doesn't respond to itself
    if message.author == client.user:
        return
    await client.process_commands(message)
        

#TODO
#spotify = discord.Spotify()


@client.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))
    else:
        await ctx.send('Yes, {0.subcommand_passed} is cool'.format(ctx))


@client.command()
async def guess(ctx, number: int):
    await ctx.send('Guess a number between 1 and 10.')

    value = random.randint(1, 6)

    await ctx.send(value == number)


@client.command()
async def hello(ctx, name: str):
    await ctx.send("Hello, {}".format(name))

@client.command()
async def add(ctx, left: int, right: int):
    "Adds two numbers together"
    await ctx.send(left + right)

@client.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

#TODO
# @client.command()
# async def lyrics(ctx, artist: str, song: str):
#     p = os.popen("./lyricsDown.sh {} {}".format(artist,song))
#     output = p.read()
#     if(len(output) > 2000):
#         await ctx.send("Sorry, that song is too long. All discord messages must have 2000 characters or less. This one has {}".format(str(len(output))))
        
#     else:
#         await ctx.send(output)

@client.command()
async def test(ctx, *args):
    artist = args[0].replace(" ","")
    song = args[1].replace(" ","")
    await ctx.send("{} {}".format(artist,song))
    
@client.command()
async def lyrics(ctx, *args):
    artist = args[0].replace(" ","")
    song = args[1].replace(" ","")
    p = os.popen("./lyricsDown.sh {} {}".format(artist,song))
    output = p.read()
    if(len(output) > 2000):
        await ctx.send("Sorry, that song is too long. All discord messages must have 2000 characters or less. This one has {}".format(str(len(output))))
        
    else:
        await ctx.send(output)



@client.command()
async def spotify(ctx, user: discord.Member=None):
    #user = user or ctx.author
    user = ctx.author
    for activity in user.activities:
        if isinstance(activity, discord.Spotify):
            await ctx.send(f"{user} is listening to {activity.title} by {activity.artist}")
            await ctx.send(activity.album_cover_url)
            await lyrics(ctx, str(activity.artist),str(activity.title))










#DO NOT CHANGE
client.run(token[0])