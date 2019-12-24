# bot.py
import os
import random

import discord
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

client = discord.Client()


@client.event
async def on_ready():
    print(f"{client.user.name} has connected to Discord!")


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Hi {member.name}, welcome to my Discord server!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    response = f'User {message.author} has said "{message.content}"'
    await message.channel.send(response)


client.run(token)
