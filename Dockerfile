FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY Pipfile* ./
RUN pip install pipenv && pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app
EXPOSE 8000

