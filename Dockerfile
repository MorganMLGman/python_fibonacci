# syntax=docker/dockerfile:1.2

FROM python:3.9.16-alpine3.17

WORKDIR /app

COPY main.py .

CMD ["python", "main.py"]