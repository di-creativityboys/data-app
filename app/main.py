import sys
import os

if os.environ.get("MY_PRODUCTION") == "production":
    sys.path.insert(0, "/app/app/")
else:
    sys.path.insert(0, "/workspaces/data-app/app/")

import json
from flask import Flask

app = Flask(__name__)

from database.database import Database
from news_scrape.bbc import bbc_etl as bbc
from news_scrape.cnn import cnn_etl as cnn
from social_media_scraping.twitter import load_tweets_db as twitter
from social_media_scraping.twitter.v2.twitter_etl import twitter_etl
from news_clustering.cluster_news_etl import cluster_articles_in_db


@app.route("/")
async def index():
    return json.dumps({"status": "data-app is running"})


@app.route("/init/")
async def myinit():
    database = Database()
    database.open_connection()
    database.initialize_schema()
    database.close_connection()

    return json.dumps({"status": "database initialized"})


@app.route("/bbc/")
async def bbc_handler():
    # Fire and forget
    await bbc.bbc_etl()

    return json.dumps({"status": "finished bbc scraping"})


@app.route("/cnn/")
async def cnn_handler():
    # Fire and forget
    await cnn.cnn_etl()

    return json.dumps({"status": "finished cnn scraping"})


@app.route("/twitter/<name>")
async def twitter_handler(name):
    # Fire and forget
    await twitter.scrape_twitter(user_name=name, limit=100)

    return json.dumps({"status": "finished twitter scraping"})


@app.route("/twitter/v2/<name>")
async def twitter_handler_v2(name):
    # Fire and forget
    await twitter_etl(steps=20, user=name)

    return json.dumps({"status": "finished twitter scraping"})


@app.route("/news/cluster")
async def cluster_handler():
    # Fire and forget
    await cluster_articles_in_db()

    return json.dumps({"status": "finished article clustering"})


if __name__ == "__main__":
    app.run(debug=False)
