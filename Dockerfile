FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app
WORKDIR /app

RUN pip install poetry
COPY pyproject.toml poetry.lock /app
RUN poetry install --no-root --no-dev

COPY sletmaster /app/sletmaster

CMD poetry run uvicorn sletmaster.main:app --port 8000 --host 0.0.0.0