import json
import psycopg2
import os
from flask import Flask
app = Flask(__name__)

from news_scrape.bbc import bbc
from news_scrape.cnn import scraper as cnn
from social_media_scraping.twitter import load_tweets_db as twitter

@app.route('/')
async def index():
    return json.dumps({'name': 'alice',
                       'email': 'alice@outlook.com'})

@app.route('/init/')
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
async def bbc_handler():
    await bbc.get_bbc_news()

    return json.dumps({'status': 'started bbc scraping'})

@app.route('/cnn/')
async def cnn_handler():
    await cnn.cnn_scraper()

    return json.dumps({'status': 'started cnn scraping'})


@app.route('/twitter/<name>')
async def scrape_twitter_api(name):
    print(f"Twitter scraping: {name}")
    await twitter.scrape_twitter(name, 100)

    return json.dumps({'status': 'started twitter scraping'})



if __name__ == "__main__":
    app.run(debug=True)
