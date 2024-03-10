FROM python:3.9

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV RABBIT_URI="amqp://admin:admin@host.docker.internal:5672/%2F"

CMD cd src && exec bash

# CMD uvicorn main:app




