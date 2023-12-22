import sys
import os

if os.environ.get("MY_PRODUCTION") == "production":
    sys.path.insert(0, "/app/app/")
else:
    sys.path.insert(0, "/workspaces/data-app/app/")

import json
import psycopg2

from flask import Flask

app = Flask(__name__)

from news_scrape.bbc import bbc_etl
from news_scrape.cnn import scraper as cnn
from social_media_scraping.twitter import load_tweets_db as twitter


@app.route("/")
async def index():
    return json.dumps({"name": "alice", "email": "alice@outlook.com"})


@app.route("/init/")
async def myinit():
    DB_PORT: str = os.environ.get("DATABASE_PORT", "5432")
    DB_HOST: str = os.environ.get("DATABASE_HOST", "localhost")

    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", port=DB_PORT, host=DB_HOST)
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(query=open(file="./database.sql", mode="r").read())

    conn.close()

    return json.dumps({"status": "ok"})


@app.route("/bbc/")
async def bbc_handler():
    bbc_etl.bbc_etl()

    return json.dumps({"status": "started bbc scraping"})


@app.route("/cnn/")
async def cnn_handler():
    await cnn.cnn_scraper()

    return json.dumps({"status": "started cnn scraping"})


@app.route("/twitter/<name>")
async def scrape_twitter_api(name):
    print(f"Twitter scraping: {name}")
    await twitter.scrape_twitter(name, 100)

    return json.dumps({"status": "started twitter scraping"})


if __name__ == "__main__":
    app.run(debug=False)
