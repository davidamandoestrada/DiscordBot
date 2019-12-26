FROM python:3.7-slim-buster 
WORKDIR /code
RUN apt-get update
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN alembic init alembic
COPY . .
RUN chmod +x ./start.sh
CMD ["./start.sh"]