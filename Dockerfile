# syntax=docker/dockerfile:1

FROM python:3.10-slim-bullseye

RUN apt update -y && apt install -y build-essential libpq-dev
ENV POETRY_VERSION=1.2.0
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --only main

COPY . .

EXPOSE 5000
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:5000", "ury_wrapped.web:app"]
