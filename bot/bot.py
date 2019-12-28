import os
import requests
import io
import aiohttp
import urllib

import discord
from discord.ext import commands
from dotenv import load_dotenv

COMMAND_PREFIX = "!"

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
processor = f'http://{os.getenv("PROCESSOR_URL")}:80'

bot = commands.Bot(command_prefix=COMMAND_PREFIX)


@bot.listen()
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.listen()
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Hi {member.name}, welcome to my Discord server!")


@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith(COMMAND_PREFIX):
        return

    session = requests.Session()
    payload = {
        "author": str(message.author),
        "avatar_url": str(message.author.avatar_url),
        "guild": message.guild.name,
        "content": message.content,
    }

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


@bot.command(name="Image")
async def on_image_command(ctx):
    session = requests.Session()
    payload = {
        "author": str(ctx.author),
        "avatar_url": str(ctx.author.avatar_url),
        "guild": ctx.guild.name,
    }
    try:
        response = session.get(f"{processor}/image/", json=payload)
        if response.status_code == 200:
            error = response.json()["error"]
            if error is None:
                await _send_avatar_image_to_discord(ctx)
            else:
                response_message = f"An error has occurred while processing this message. Error: {error}"
                await ctx.send(response_message)
        else:
            await ctx.send(response)
    except Exception as exception:
        await ctx.send(f"ERROR: {exception}")


async def _send_avatar_image_to_discord(ctx):
    async with aiohttp.ClientSession() as session:
        avatar_file_name_url_safe = urllib.parse.quote(
            f"{ctx.author}_avatar.jpg", safe=""
        )
        async with session.get(
            f"https://shodanbot.s3-us-west-1.amazonaws.com/{avatar_file_name_url_safe}"
        ) as resp:
            if resp.status != 200:
                return await ctx.send("Could not download file...")
            data = io.BytesIO(await resp.read())
            await ctx.send(file=discord.File(data, avatar_file_name_url_safe,))


bot.run(token)
