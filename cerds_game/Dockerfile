FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update && apk add --no-cache \
    gcc musl-dev postgresql-dev python3-dev libffi-dev \
    cargo jpeg-dev zlib-dev

WORKDIR /app

# Встановлення залежностей напряму (не рекомендовано для великих проєктів)
RUN pip install --upgrade pip && pip install \
    "Django>=4.0" \
    daphne \
    channels \
    channels_redis \
    psycopg2 \
    django-cors-headers \
    django-environ \
    python-decouple \
    djangorestframework \
    requests

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && daphne -b 0.0.0.0 -p 8000 cerds_game.asgi:application"]
