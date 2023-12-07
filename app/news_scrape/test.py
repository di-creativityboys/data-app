import asyncio
import psycopg2
from bbc.bbc import get_bbc_news
from cnn import scraper as cnn
import os

DB_PORT = os.environ.get("DATABASE_PORT", "5432")
DB_HOST = os.environ.get("DATABASE_HOST", "localhost")

def manual_db_init():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", port=DB_PORT, host=DB_HOST)
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(open("./database.sql", "r").read())

    conn.close()
    print("DB initialized")

async def main():
    manual_db_init()
    await get_bbc_news()

    await cnn.cnn_scraper()


if __name__ == "__main__":
    asyncio.run(main())
    print('test')
