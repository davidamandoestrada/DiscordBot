import boto3
from botocore.exceptions import ClientError
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import imgkit
import logging
import urllib

from entities.message import Message
from entities.user import User, find_user_by_user_name, find_users, UserNotFoundError

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
        User.create_new(image_command.author)
        user = find_user_by_user_name(image_command.author)
    file_name = _create_image(image_command, user)
    _upload_image_to_s3(file_name=file_name, bucket="shodanbot")
    return {"response_message": None, "error": None}


class IncomingMessage(BaseModel):
    author: str
    avatar_url: str
    guild: str
    content: str


@app.get("/message/")
def process_message(message: IncomingMessage):
    _store_message(message)
    return _shodan_message(message)


def _upload_image_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client("s3")
    try:
        s3_client.upload_file(
            file_name, bucket, object_name, ExtraArgs={"ContentType": "image/jpeg"}
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True


def _create_image(message: IncomingMessage, user: User):
    options = {
        "format": "jpg",
        "crop-h": "338",
        "crop-y": "12",
        "crop-w": "326",
        "crop-x": "12",
        "disable-smart-width": "",
        "width": 350,
        "encoding": "UTF-8",
    }
    file_name = f"{message.author}_avatar.jpg"
    safe_author = urllib.parse.quote(message.author, safe="")
    safe_guild_name = urllib.parse.quote(message.guild, safe="")
    level_url = urllib.parse.quote("https://i.redd.it/ct3wm41ws8021.jpg", safe="")
    avatar_url = urllib.parse.quote(user.avatar_url, safe="")
    exp = 5_000_000
    level = 1_000_000
    imgkit.from_url(
        f"http://avatar:5000/avatar/{safe_author}/{safe_guild_name}/{avatar_url}/{level_url}/{exp}/{level}",
        file_name,
        options=options,
    )

    return file_name


def _shodan_message(message: IncomingMessage):
    session = requests.Session()
    headers = {"content-type": "application/json"}
    return session.get(
        f"http://shodan-bot:8080/message/", data=message.json(), headers=headers
    ).json()


def _store_message(message: IncomingMessage):
    try:
        user = find_user_by_user_name(message.author)
    except UserNotFoundError:
        User.create_new(message.author)
        user = find_user_by_user_name(message.author)
    Message.create_new(user, message.content)
    return {"response_message": None, "error": None}
