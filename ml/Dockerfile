FROM python:3.9.18

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD exec python ml_service.py

