FROM python:3.9
RUN apt update && apt install nginx tree -y --no-install-recommends

COPY . .

RUN apt install pipenv -y && pipenv install

