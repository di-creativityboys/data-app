import json
from flask import Flask
app = Flask(__name__)

from news_scrape.bbc.bbc import get_bbc_news

@app.route('/')
async def index():


    return json.dumps({'name': 'alice',
                       'email': 'alice@outlook.com'})

import psycopg2
import os

@app.route('/myinit/')
async def myinit():
    print(os.getcwd())

    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", port="5432", host="localhost")
    conn.autocommit = True

    cursor = conn.cursor()

    cursor.execute(open("./database.sql", "r").read())

    conn.close()


    return json.dumps({'name': 'ok',
                       'email': 'alice@outlook.com'})

@app.route('/bbc/')
async def bbc():
    get_bbc_news()

    return json.dumps({'name': 'bbc',
                       'email': 'alice@outlook.com'})



if __name__ == "__main__":
    app.run(debug=True)