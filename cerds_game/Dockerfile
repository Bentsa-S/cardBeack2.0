FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Залежності
RUN apk update && apk add --no-cache \
    gcc musl-dev postgresql-dev python3-dev libffi-dev \
    cargo jpeg-dev zlib-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "python manage.py migrate && daphne -b 127.0.0.1 -p 8000 cerds_game.asgi:application"]
