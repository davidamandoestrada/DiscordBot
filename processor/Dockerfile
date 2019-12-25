FROM tiangolo/uvicorn-gunicorn:python3.7
RUN apt-get update
RUN apt-get -y install gcc
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /app