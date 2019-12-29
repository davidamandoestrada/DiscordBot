FROM tiangolo/uvicorn-gunicorn:python3.7
RUN apt-get update
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV WEB_CONCURRENCY=1
COPY ./app /app
COPY . .