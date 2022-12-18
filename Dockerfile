# syntax=docker/dockerfile:1.4

FROM python:3.9.16-alpine3.17

WORKDIR /app

RUN pip install --no-cache-dir redis

COPY main.py .

CMD ["python", "main.py"]