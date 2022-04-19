# syntax=docker/dockerfile:1

FROM python:3.9.12-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y git

RUN pip3 install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["scrapy"]

##useful commands  docker run -it -v ${PWD}:/app ufc-stats-scraper crawl ufc_future_fights  -o future.csv -t csv this will output csv file in current directory
