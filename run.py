#!/usr/bin/python

import sys
import discord
import os
from dotenv import load_dotenv

load_dotenv()

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

intents = discord.Intents.default()
intents.message_content = True

activity = discord.Activity(type=discord.ActivityType.watching, name='you >:)')
client = discord.Client(intents=intents, activity=activity)

async def send_dad_joke(response, channel):
    if response.lower() == 'goober':
        await channel.send(f'No I am goober >:(')
        return
    # await channel.send(f'Hi, {response}. I\'m ' + client.user.name)
    await channel.send(f'Hi, {response}. I\'m goober')

@client.event
async def on_ready():
    channel = client.get_channel(1092119393246384151)
    await channel.send('helo')

@client.event
async def on_message(message):
    # don't respond to self
    if message.author == client.user:
        return

    # make everything lower case and remove duplicate whitespace
    lower = message.content.lower()
    lower = lower.replace(chr(0x2018), '\'').replace(chr(0x2019), '\'')
    cleaned = ' '.join(lower.split())

    # cat stuff
    if 'cat' in cleaned:
        if message.author.id == 450923244346802176:
            await message.channel.send('*insert insults here*')
            return
        await message.channel.send('meow')
        return
    if 'meow' in cleaned:
        await message.channel.send('Hey, that\'s my line :(')
        return

    # dad jokes
    if " i'm " in cleaned or cleaned[:4] == "i'm ":
        index = lower.find('i\'m') + 3
        response = message.content[index:]
        while str.isspace(response[0]):
            response = response[1:]
        await send_dad_joke(response, message.channel)
        return
    if " i am " in cleaned or cleaned[:5] == "i am ":
        # find the index of the first non-whitespace character after 'i am'
        index = 0
        while True:
            if (index == 0 or str.isspace(lower[index-1])) and lower[index:].split()[:2] == ['i', 'am']:
                index += lower[index:].find('am') + 2
                while str.isspace(lower[index]):
                    index += 1
                    if index == len(lower):
                        eprint(f"oh no, this message broke me with whitespace: {message.content}")
                        index = -1
                        break
                break
            index += lower[index + 1:].find('i') + 1
            if index >= len(lower):
                eprint(f"oh no, this message broke me in a mysterious way: {message.content}")
                index = -1
                break

        if index != -1:
            response = message.content[index:]
            await send_dad_joke(response, message.channel)
        return

eprint('args:', sys.argv)
client.run(os.environ['DISCORD_KEY'])
