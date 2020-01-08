from pydantic import BaseModel

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["bot"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chatbot = ChatBot("Shodan Bot")

trained = False


class IncomingMessage(BaseModel):
    content: str


@app.get("/message/")
def process_message(message: IncomingMessage):
    global trained
    if trained is False:
        trainer = ChatterBotCorpusTrainer(chatbot)
        trainer.train("chatterbot.corpus.english")
        trainer.train("chatterbot.corpus.english.greetings")
        trainer.train("chatterbot.corpus.english.conversations")
        trained = True

    try:
        return {
            "response_message": str(chatbot.get_response(message.content)),
            "error": None,
        }
    except Exception as e:
        return {"response_message": str(e), "error": True}
