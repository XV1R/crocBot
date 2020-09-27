import discord
from discord.ext import commands
from discord import Spotify
import random
import asyncio
import subprocess
import os
import json

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy import SpotifyClientCredentials

from extra_commands import spotipy_func as spot


description = "My first bot; works as a testing ground"
#the bot instance
client = commands.Bot(command_prefix='$', description=description)



token = open('token.txt')
token = token.readlines()



@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    print(client.user.name)
    print('------------')

@client.event
async def on_message(message):
    #makes sure the bot doesn't respond to itself
    if message.author == client.user:
        return
    await client.process_commands(message)
        

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
            return
    await ctx.send("No song playing currently")

@client.command()
async def playlists(ctx, *args):
    user = ctx.author
    if len(args) < 1:
        await ctx.send("Empty username; please enter a spotify username!")
        return
    spotify_user = str(args[0]).strip()
    playlists,sp = spot.playlists(spotify_user,user)

    while playlists:
        for i, playlist in enumerate(playlists['items']):
            embeddedMessage = discord.Embed(
                title=playlist['name'],
                description=f"{spotify_user} follows {playlist['name']}",
                colour=discord.Colour.from_rgb(
                        random.randint(0,255),
                        random.randint(0,255),
                        random.randint(0,255)
                        ),
                    )
            embeddedMessage.set_author(name=user)
            embeddedMessage.set_image(url=playlist['images'][0]['url'])
            embeddedMessage.set_thumbnail(url=playlist['images'][0]['url'])
            await ctx.send(embed=embeddedMessage)
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None

@client.command()
async def pin(ctx, *args):
    if len(args) < 2:
        await ctx.send("Sorry, couldn't store that image. Please make sure you named it along with a link to the image")
        return
    name = str(args[0]).strip()
    link = str(args[1]).strip()
    if link.startswith("https://") != True or len(link) <= len("https://"):
        await ctx.send("Not a valid Image URL. Try again.")
        return

    author = ctx.author.name 
    with open("images.json") as f:
        data = json.load(f)
    data["images"][name] = {"name":name,"url":link,"author":author}
    f = open("images.json","w")
    json.dump(data,f,ensure_ascii=False,indent=2)

    await ctx.send(f"Now storing {link} as {name}")
    data.close()

@client.command()
async def unpin(ctx, *args):
    if len(args) < 1:
        await ctx.send("Sorry, couldn't remove that image. Please make sure you have a proper name.")
        return
    name = str(args[0]).strip()
        
    with open("images.json") as f:
        data = json.load(f)
    await ctx.send(f"{data['images'][name]['name']} has been removed; LINK: {data['images'][name]['url']}")
    del data["images"][name] 
    f = open("images.json","w")
    json.dump(data,f,ensure_ascii=False,indent=2)
    
    data.close()

@client.command()
async def fetch(ctx, *args):
    if len(args) < 1:
        await ctx.send("Sorry, cannot fetch an image without its name.")
        return
    name = str(args[0]).strip()
    with open("images.json") as f:
        file = json.load(f)
    embeddedMessage = discord.Embed(
        title = file["images"][name]["name"],
        colour=discord.Colour.from_rgb(
                random.randint(0,255),
                random.randint(0,255),
                random.randint(0,255)
                ),
    )
    embeddedMessage.set_image(url=file["images"][name]["url"])
    embeddedMessage.set_author(name=file["images"][name]["author"])
    await ctx.send(embed=embeddedMessage)
    f.close()


@client.command()
async def pinned(ctx): 
    with open("images.json") as f:
        data = json.load(f)
    await ctx.send(f"----Currenly stored----")
    for image in data['images']:
        await ctx.send(f"{data['images'][image]['name']} -> pinned by {data['images'][image]['author']}")

@client.command()
async def related_artists(ctx):
    kendrick = "spotify:artist:2YZyLoL8N0Wb9xBt1NhZWg"
    data = spot.related(kendrick)
    with open("artists.json","w") as f:
        json.dump(data,f,indent=2)
    

    
    




#DO NOT CHANGE
client.run(token[0])
