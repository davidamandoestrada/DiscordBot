import os

CHATBOT_URL = "http://chatbot:80"
PROCESSOR_URL = f'http://{os.getenv("PROCESSOR_URL")}:80'
COMMAND_PREFIX = "!"
TOKEN = os.getenv("DISCORD_TOKEN")
S3_URL = "https://shodanbot.s3-us-west-1.amazonaws.com"