import os
import requests

import discord
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
processor = f'http://{os.getenv("PROCESSOR_URL")}:80'

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

    session = requests.Session()
    payload = {"author": str(message.author), "content": message.content}

    try:
        response = session.get(f"{processor}/message/", json=payload)
        if response.status_code == 200:
            response_message = response.json()["response_message"]
            error = response.json()["error"]
            if error is None:
                if response_message:
                    await message.channel.send(response_message)
            else:
                response_message = f"An error has occurred while processing this message. Error: {error}"
                await message.channel.send(response_message)
        else:
            await message.channel.send(response)
    except Exception as exception:
        await message.channel.send(f"ERROR: {exception}")


client.run(token)
