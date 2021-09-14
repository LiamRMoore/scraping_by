# Scraping By

Web scraper application for identifying public sector contracts. 

Currently implemented:
    
    - (Public Contracts Scotland)[https://www.publiccontractsscotland.gov.uk/] **under construction**

## Install

Install the python environment for the webscraper:

```bash
conda env create -f env.yml
```

Activate the environment:

```
conda activate scraping_by
```

Install the docker container running a Splash server (for scraping
dynamic webpages), and pSQL + pgAdmin (for storing scraped data).

```bash
docker-compose up -d
```

## Run webscraper

```bash
scrapy crawl notices
```

### docker-compose details
This Compose file contains the following environment variables:

* `POSTGRES_USER` the default value is **postgres**
* `POSTGRES_PASSWORD` the default value is **changeme**
* `PGADMIN_PORT` the default value is **5050**
* `PGADMIN_DEFAULT_EMAIL` the default value is **pgadmin4@pgadmin.org**
* `PGADMIN_DEFAULT_PASSWORD` the default value is **admin**

## Access to postgres: 
* `localhost:5432`
* **Username:** postgres (as a default)
* **Password:** changeme (as a default)

## Access to PgAdmin: 
* **URL:** `http://localhost:5050`
* **Username:** pgadmin4@pgadmin.org (as a default)
* **Password:** admin (as a default)

## Access to Splash:

* **URL:** `http:localhost:8050`

## Add a new server in PgAdmin:
* **Host name/address** `postgres`
* **Port** `5432`
* **Username** as `POSTGRES_USER`, by default: `postgres`
* **Password** as `POSTGRES_PASSWORD`, by default `changeme`


