from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

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


class IncomingMessage(BaseModel):
    author: str
    content: str


@app.get("/message/")
def process_message(message: IncomingMessage):
    if "Playback" in message.content:
        response = ["The following is a list of messages that have been recorded:"]
        users = find_users()
        for user in users:
            response.append(f"User {user.user_name} has said:")
            for message in user.messages:
                response.append(message.content)
        return {"response_message": "\n".join(response), "error": None}
    else:
        try:
            user = find_user_by_user_name(message.author)
        except UserNotFoundError:
            user = User.create_new(message.author)
        Message.create_new(message.author, message.content)
        return {"response_message": None, "error": None}
