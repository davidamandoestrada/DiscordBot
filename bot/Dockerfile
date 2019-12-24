FROM python:3.7-slim-buster
ARG DISCORD_TOKEN
ARG PROCESSOR_URL
WORKDIR /code
ENV DISCORD_TOKEN=${DISCORD_TOKEN}
ENV PROCESSOR_URL=${PROCESSOR_URL}
RUN apt-get update
RUN apt-get -y install gcc
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "bot.py"]