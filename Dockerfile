FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --system

COPY ./Entrypoint.sh .
RUN chmod +x /app/Entrypoint.sh

COPY . .

EXPOSE 8000

ENTRYPOINT ["/app/Entrypoint.sh"]
