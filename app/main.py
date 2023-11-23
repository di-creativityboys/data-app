import json
import psycopg2
import os
from flask import Flask
app = Flask(__name__)

from .news_scrape.bbc.bbc import get_bbc_news
from .news_scrape.cnn.scraper import scrape_from_cnn

from .social_media_scraping.twitter.load_tweets_db import scrape_twitter

@app.route('/')
async def index():
    return json.dumps({'name': 'alice',
                       'email': 'alice@outlook.com'})

@app.route('/myinit/')
async def myinit():
    DB_PORT = os.environ.get("DATABASE_PORT", "5432")
    DB_HOST = os.environ.get("DATABASE_HOST", "localhost")


    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", port=DB_PORT, host=DB_HOST)
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(open("./database.sql", "r").read())

    conn.close()

    return json.dumps({'status': 'ok'})

@app.route('/bbc/')
async def bbc():
    await get_bbc_news()

    return json.dumps({'status': 'started bbc scraping'})

@app.route('/cnn/')
async def cnn():
    await scrape_from_cnn()

    return json.dumps({'status': 'started cnn scraping'})


@app.route('/twitter/<name>')
async def scrape_twitter_api(name):
    print(f"Twitter scraping: {name}")
    await scrape_twitter(name, 100)

    return json.dumps({'status': 'started twitter scraping'})



if __name__ == "__main__":
    app.run(debug=True)