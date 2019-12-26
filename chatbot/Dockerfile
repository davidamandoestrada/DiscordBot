FROM tiangolo/uvicorn-gunicorn:python3.7
RUN apt-get update
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./app /app