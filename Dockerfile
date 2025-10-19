FROM python:3.12-alpine3.22

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update && apk add --no-cache \
    build-base \
    postgresql-dev \
 && rm -rf /var/cache/apk/*

RUN pip install uv

COPY ./requirements.txt .

RUN uv pip install --no-cache-dir -r requirements.txt --system

COPY . .

EXPOSE 8000

CMD alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000