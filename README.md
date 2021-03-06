# ufc-stats-scraper

ufc-stats-scraper is a python project that scraps data from [ufcstats.com](http://ufcstats.com/statistics/events/completed) and normalizes the data. It uses the popular library [scrapy](https://scrapy.org/) to extract fighter data, past-fight data, and future-fight data so the data can be used in a future ML project to predict future fights based off of the tale-of-the-tape.

## Getting Started
ufc-stats-scraper can be cloned from GitHub or downloaded from Docker Hub

## Python 
This project can be cloned and run as a Python program. The only prerequisite is that you must have Python 3 installed on your system. Follow the following steps to get your system setup:

- Create a [virtualenv](https://docs.python.org/3/tutorial/venv.html) for the project
- Activate your virtual env
- install all the required dependencies - `pip install -r requirements.txt`

After the setup is complete, the following commands will create csv files with the scraped data:

```
scrapy crawl ufc_fighters -o fighters.csv -t csv
scrapy crawl ufc_fights -o fights.csv -t csv
scrapy crawl ufc_future_fights -o future_fights.csv -t csv
```

## Database Pipelines

Scrapy pipelines have been setup to commit scraped data to a MySQL database. If this functionality is desired, then please set the following variables for your envrionment:

```
DB_USER=<some DB user>
DB_PASSWORD=<password for DB user>
DB_HOST=<host for the DB>
DB_DATABASE=<some DB name>
```

If no DB variables are provided, then the pipelines just return the scraped items.

## Docker

https://hub.docker.com/repository/docker/natebuel29/ufc-stats-scraper

ufc-stats-scraper has also been containerized and made avaliable on Docker Hub. The following commands can be used to kick off the web scraper and extract the csv file from the container:

```
docker run -it -v ${PWD}:/app/data natebuel29/ufc-stats-scraper  scrapy crawl ufc_fighters -o /app/data/fighters.csv -t csv
docker run -it -v ${PWD}:/app/data natebuel29/ufc-stats-scraper  scrapy crawl ufc_fights -o /app/data/fights.csv -t csv
docker run -it -v ${PWD}:/app/data natebuel29/ufc-stats-scraper  scrapy crawl ufc_future_fights -o /app/data/future_fights.csv -t csv
```

NOTE: The docker run command needs to mount the /app/data directory to acquire the csv output files. `${PWD}:/app/data` mounts the current directory to the containers app/data directory.

The `--env` docker flag can be used to pass in the the DB environment variables to the docker container if you have a DB to commit data to. The following commands can be used to kick off the web scraper and commit the data to a DB:

```
docker run -it --env DB_HOST=<DB host> --env DB_USER=<DB user> --env DB_PASSWORD=<DB user password> --env DB_DATABASE=<DB database> natebuel29/ufc-stats-scraper scrapy crawl ufc_fighters 
docker run -it --env DB_HOST=<DB host> --env DB_USER=<DB user> --env DB_PASSWORD=<DB user password> --env DB_DATABASE=<DB database> natebuel29/ufc-stats-scraper scrapy crawl ufc_fights 
docker run -it --env DB_HOST=<DB host> --env DB_USER=<DB user> --env DB_PASSWORD=<DB user password> --env DB_DATABASE=<DB database> natebuel29/ufc-stats-scraper scrapy crawl ufc_future_fights 

```

## Testing

There are some very simple unit tests written to verify that the extracted data is valid. This tests can be run by the command `python3 unittest`.

## TODO

- [x] Send scraped data to a database (MySQL)
    - [ ] Once the DB is setup, scrape events only within the past week. It can run every Sunday (fight nights are on Saturday) and can scrape the fight data from the previous weeks event.
- [ ] Figure out a way to make the DockerFile commands easier (maybe MakeFile?)
- [ ] Create a main program that kicks off all three spiders
 