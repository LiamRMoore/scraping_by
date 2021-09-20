FROM continuumio/miniconda3 as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app.py app.py
COPY scraping_by ./scraping_by
COPY env.yml env.yml

RUN conda env create -f env.yml
CMD ["conda", "run", "--no-capture-output", "-n", "scraping_by", \
    "uvicorn", "--reload", "app:app", "--host", "0.0.0.0", "--port", "80"]