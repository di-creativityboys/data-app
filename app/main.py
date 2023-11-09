import json
import psycopg2
import os
from flask import Flask
app = Flask(__name__)

from news_scrape.bbc.bbc import get_bbc_news

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

    return json.dumps({'status': 'started scraping'})



if __name__ == "__main__":
    app.run(debug=True)