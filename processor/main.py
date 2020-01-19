import logging
from typing import Optional
import urllib

import requests
from botocore.exceptions import ClientError
from pydantic import BaseModel

import boto3
import imgkit
from entities.message import Message
from entities.user import (User, UserNotFoundError, find_user_by_user_name,
                           find_users)
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# Constants
AVATAR_CREATION_SERVICE_URL = "http://avatar:5000"
CHATBOT_URL = "http://chatbot:80"
PROFANITY_POLITICS_FILTER_URL = "http://profanity-poltics-filter:8080"
IMAGE_OPTIONS = options = {
        "format": "jpg",
        "crop-h": "338",
        "crop-y": "12",
        "crop-w": "326",
        "crop-x": "12",
        "disable-smart-width": "",
        "width": 350,
        "encoding": "UTF-8",
    }
LEVEL_URL = "https://i.redd.it/ct3wm41ws8021.jpg"

app = FastAPI()

origins = ["bot"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ImageCommand(BaseModel):
    author: str
    avatar_url: str
    guild: str


@app.get("/playback/")
def process_playback():
    response = ["The following is a list of messages that have been recorded:"]
    users = find_users()
    for user in users:
        response.append(f"User {user.user_name} has said:")
        for message in user.messages:
            response.append(f"{message.date_time}: {message.content}")
    return {"response_message": "\n".join(response), "error": None}


@app.get("/image/")
def process_image_command(image_command: ImageCommand):
    try:
        user = find_user_by_user_name(image_command.author)
        user.avatar_url = image_command.avatar_url
    except UserNotFoundError:
        User.create_new(image_command.author, image_command.avatar_url)
        user = find_user_by_user_name(image_command.author)

    file_name = f"{image_command.author}_avatar.jpg"
    _create_image(message=image_command, user=user, file_name=file_name)

    try:
        _upload_image_to_s3(file_name=file_name, bucket="shodanbot")
        return {"response_message": None, "error": None}
    except Exception as error:
        return {"response_message": str(error), "error": True}


class IncomingMessage(BaseModel):
    author: str
    avatar_url: str
    guild: Optional[str] = None
    content: str
    type_of_message: str


@app.get("/message/")
def process_message(message: IncomingMessage):
    _store_message(message)
    if message.type_of_message == "non-private":
        return _profanity_and_politics_filter_message(message)
    elif message.type_of_message == "private":
        return _chatbot_message(message)


def _upload_image_to_s3(file_name, bucket):
    s3_client = boto3.client("s3")
    try:
        s3_client.upload_file(
            file_name, bucket, file_name, ExtraArgs={"ContentType":
                                                     "image/jpeg"}
        )
    except ClientError as error:
        logging.error(error)
        raise error


def _create_image(message: ImageCommand, user: User, file_name: str):
    safe_author = urllib.parse.quote(message.author, safe="")
    safe_guild_name = urllib.parse.quote(message.guild, safe="")
    safe_avatar_url = urllib.parse.quote(user.avatar_url, safe="")
    safe_level_url = urllib.parse.quote(LEVEL_URL,
                                        safe="")
    exp = user.exp - user.exp_for_level(user.level)
    level = user.level

    avatar_creation_service_url_parameters = [safe_author, safe_guild_name,
                                              safe_avatar_url, safe_level_url,
                                              str(exp), str(level)]
    imgkit.from_url(
        f"{AVATAR_CREATION_SERVICE_URL}/avatar/"
        f"{'/'.join(avatar_creation_service_url_parameters)}",
        file_name,
        options=IMAGE_OPTIONS,
    )

    return file_name


def _profanity_and_politics_filter_message(message: IncomingMessage):
    session = requests.Session()
    headers = {"content-type": "application/json"}
    return session.get(
        f"{PROFANITY_POLITICS_FILTER_URL}/message/", data=message.json(), headers=headers
    ).json()


def _chatbot_message(message: IncomingMessage):
    session = requests.Session()
    headers = {"content-type": "application/json"}
    return session.get(
        f"{CHATBOT_URL}/message/", data=message.json(), headers=headers
    ).json()


def _store_message(message: IncomingMessage):
    try:
        user = find_user_by_user_name(message.author)
    except UserNotFoundError:
        User.create_new(message.author)
        user = find_user_by_user_name(message.author)
    Message.create_new(user, message.content)
    return {"response_message": None, "error": None}
