import requests

from constants import CHATBOT_URL, PROCESSOR_URL


async def handle_private_message(message):
    async def respond_to_private_message(response_message):
        await message.author.create_dm()
        await message.author.dm_channel.send(response_message)

    session = requests.Session()
    payload = {
        "content": message.content,
    }
    try:
        response = session.get(f"{CHATBOT_URL}/message/", json=payload)
        function_to_use_to_respond = respond_to_private_message
        await _handle_message_response(response, function_to_use_to_respond)
    except Exception as exception:
        await message.author.create_dm()
        await message.author.dm_channel.send(f"ERROR: {exception}")


async def handle_non_private_message(message):
    session = requests.Session()
    payload = {
        "author": str(message.author),
        "avatar_url": str(message.author.avatar_url),
        "guild": message.guild.name,
        "content": message.content,
    }

    try:
        response = session.get(f"{PROCESSOR_URL}/message/", json=payload)
        function_to_use_to_respond = message.channel.send
        await _handle_message_response(response, function_to_use_to_respond)
    except Exception as exception:
        await message.channel.send(f"ERROR: {exception}")


async def _handle_message_response(response, function_to_use_to_respond):
    if response.status_code == 200:
        response_message = response.json()["response_message"]
        error = response.json()["error"]
        if error is None:
            if response_message:
                await function_to_use_to_respond(response_message)
        else:
            response_message = (
                "An error has occurred while processing this message."
                f" Error: {error}"
            )
            await function_to_use_to_respond(response_message)
    else:
        await function_to_use_to_respond(response)
