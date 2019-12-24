FROM python:3.7-slim-buster
WORKDIR /code
RUN apt-get update
RUN apt-get -y install gcc
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "processor:app", "--reload"]