import discord
import random
import asyncio

#the bot instance
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    #makes sure the bot doesn't respond to itself
    if message.author == client.user:
        return
        

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('$ping'):
        await message.channel.send('pong')

    if message.content.startswith('$guess'):
        await message.channel.send('Guess a number between 1 and 10.')
    
        def is_correct(m):
            return m.author == message.author and m.content.isdigit()

        answer = random.randint(1,10)
        print(answer)

        try:
            #waits 10 seconds for a response 
            guess = await client.wait_for('message', check=is_correct, timeout=10.0)
        except asyncio.TimeoutError:
            return await message.channel.send('Sorry, you took too long. It was {}.'.format(answer))
        
        if int(guess.content) == answer:
            await message.channel.send("You're right! The number was {}".format(answer))
        else:
            await message.channel.send("Oops. It's actually {}".format(answer))

#DO NOT CHANGE
client.run("Njk2Nzg4Mjk4MzMyNTA0MTE1.Xot5Cg.3mO0yfxjb5cBJAmVyGLvHT1cpDM")