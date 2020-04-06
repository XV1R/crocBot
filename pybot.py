import discord

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    #checks if the message was sent by the person who 
    # called the bot
    if message.author == client.user:
        return
        

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('$ping'):
        await message.channel.send('pong')


#DO NOT CHANGE
client.run("Njk2Nzg4Mjk4MzMyNTA0MTE1.Xot5Cg.3mO0yfxjb5cBJAmVyGLvHT1cpDM")