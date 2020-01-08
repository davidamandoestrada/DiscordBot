import io
import urllib

import requests

import aiohttp
import discord
from constants import COMMAND_PREFIX, PROCESSOR_URL, S3_URL, TOKEN
from discord.ext import commands
from dotenv import load_dotenv
from message_handlers import handle_non_private_message, handle_private_message
from utility import chunk_response_message_into_n_line_chunks

load_dotenv()


bot = commands.Bot(command_prefix=COMMAND_PREFIX)


@bot.listen()
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.listen()
async def on_member_join(member: discord.Member):
    await member.create_dm()
    await member.dm_channel.send(f"Hi {member.name},"
                                 " welcome to my Discord server!")


@bot.listen()
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    if message.content.startswith(COMMAND_PREFIX):
        return
    if message.channel.type == discord.ChannelType.private:
        await handle_private_message(message)
    else:
        await handle_non_private_message(message)


@bot.command(name="Image")
async def on_image_command(ctx: commands.context):
    session = requests.Session()
    payload = {
        "author": str(ctx.author),
        "avatar_url": str(ctx.author.avatar_url),
        "guild": ctx.guild.name,
    }

    try:
        response = session.get(f"{PROCESSOR_URL}/image/", json=payload)
        if response.status_code == 200:
            error = response.json()["error"]
            if error is None:
                await _send_avatar_image_to_discord(ctx)
        else:
            error = response
    except Exception as exception:
        error = str(exception)

    if error:
        await ctx.send(error)


@bot.command(name="Playback")
async def on_playback_command(ctx: commands.context):
    session = requests.Session()

    try:
        response = session.get(f"{PROCESSOR_URL}/playback/")
        if response.status_code == 200:
            error = response.json()["error"]
            if error is None:
                response_message = response.json()["response_message"]
                chunks = chunk_response_message_into_n_line_chunks(
                    response_message, n=10
                )
                for chunk in chunks:
                    await ctx.send("\n".join(chunk))
        else:
            error = response
    except Exception as exception:
        error = str(exception)

    if error:
        await ctx.send(error)


async def _send_avatar_image_to_discord(ctx: commands.context):
    async with aiohttp.ClientSession() as session:
        avatar_file_name_url_safe = urllib.parse.quote(
            f"{ctx.author}_avatar.jpg", safe=""
        )
        async with session.get(f"{S3_URL}/{avatar_file_name_url_safe}") as resp:
            if resp.status != 200:
                return await ctx.send("Could not download file...")
            data = io.BytesIO(await resp.read())
            await ctx.send(file=discord.File(data, avatar_file_name_url_safe,))


bot.run(TOKEN)
