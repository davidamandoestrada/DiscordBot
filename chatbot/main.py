from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["processor"]

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
    try:
        return {"response_message": "test", "error": None}
        chatbot = ChatBot("Ron Obvious")

        # Create a new trainer for the chatbot
        trainer = ChatterBotCorpusTrainer(chatbot)

        # Train the chatbot based on the english corpus
        trainer.train("chatterbot.corpus.english")

        # Get a response to an input statement
        return {
            "response_message": str(chatbot.get_response(message.content)),
            "error": None,
        }
    except Exception as e:
        return {"response_message": str(e), "error": True}

