# syntax=docker/dockerfile:1

FROM python:3.9.12-slim-buster

WORKDIR /app

RUN mkdir /data

RUN apt-get update && apt-get install -y git

RUN pip3 install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ADD . /app

CMD ["scrapy", "crawl", "ufc_future_fights","-o future.csv -t csv"]
